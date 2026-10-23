"""
jlc_query.py — search the jlcparts snapshot of JLCPCB's assembly parts library.

    python hardware/tools/jlc_query.py ADS131M04
    python hardware/tools/jlc_query.py --lcsc 2040
    python hardware/tools/jlc_query.py --cat "Amplifiers" --sub "Operational" --text "rail-to-rail" --min-stock 500

The database is ~/jlcparts/cache.sqlite3 (see hardware/README.md for how it is fetched; it is a
snapshot, refresh it before an order). `library_type` is JLC's own: "base" parts (basic) carry no
per-part setup fee on an assembled order, "expand" parts (extended) do, so prefer basic.
"""

import argparse
import json
import os
import sqlite3
import sys

DB = os.path.expanduser(os.environ.get("JLCPARTS_DB", "~/jlcparts/cache.sqlite3"))


def connect():
    if not os.path.exists(DB):
        sys.exit(f"{DB} not found; fetch the jlcparts cache first (hardware/README.md)")
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)


def unit_price(price_text, qty=5):
    """Unit price at `qty` from JLC's tier string '1-199:0.0116,200-599:0.0092,...'."""
    best = None
    for tier in price_text.split(","):
        rng, p = tier.split(":")
        lo, _, hi = rng.partition("-")
        if int(lo) <= qty and (hi == "" or qty <= int(hi)):
            best = float(p)
    return best if best is not None else float(price_text.split(",")[0].split(":")[1])


def search(text=None, lcsc=None, cat=None, sub=None, min_stock=1, basic_only=False, limit=15, qty=5, smt_only=False):
    db = connect()
    q = "select lcsc, mfr, package, library_type, stock, price, category, subcategory, description, datasheet, attributes, joints from jlc_components where present=1 and stock>=?"
    args = [min_stock]
    if lcsc:
        q += " and lcsc=?"
        args.append(int(lcsc))
    if text:
        for w in text.split():
            q += " and (mfr like ? or description like ?)"
            args += [f"%{w}%", f"%{w}%"]
    if cat:
        q += " and category like ?"
        args.append(f"%{cat}%")
    if sub:
        q += " and subcategory like ?"
        args.append(f"%{sub}%")
    if basic_only:
        q += " and library_type='base'"
    if smt_only:
        # machine-placed parts only: JLC marks through-hole parts 'THT'/'manualWeld' (hand soldered);
        # parts with no marking are accepted only when the package is not a through-hole one
        q += " and ((assembly_process='SMT' and assembly_mode='smtWeld') or (assembly_process is null and package not like '%插件%'))"
    q += " order by (library_type='base') desc, stock desc limit ?"
    args.append(limit)
    out = []
    for r in db.execute(q, args):
        lcsc_, mfr, pkg, lt, stock, price, c, s, desc, ds, attrs, joints = r
        out.append(dict(lcsc=f"C{lcsc_}", mfr=mfr, package=pkg, type="basic" if lt == "base" else "extended", stock=stock, unit_price=unit_price(price, qty), category=f"{c} / {s}", description=desc, datasheet=ds, attributes=json.loads(attrs), joints=joints))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?")
    ap.add_argument("--lcsc")
    ap.add_argument("--cat")
    ap.add_argument("--sub")
    ap.add_argument("--min-stock", type=int, default=1)
    ap.add_argument("--basic", action="store_true")
    ap.add_argument("--smt", action="store_true", help="machine-assembled SMT parts only")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--qty", type=int, default=5)
    a = ap.parse_args()
    for r in search(a.text, a.lcsc, a.cat, a.sub, a.min_stock, a.basic, a.limit, a.qty, a.smt):
        print(f"{r['lcsc']:>9} {r['type']:8s} stock {r['stock']:>8} ${r['unit_price']:.4f}  {r['mfr']:<22} {r['package']:<14} {r['description'][:90]}")


if __name__ == "__main__":
    main()
