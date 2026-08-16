#!/usr/bin/env python3
"""
spice_to_schematic.py
---------------------
Parse a subset of SPICE netlists (V, R, D elements) and render a schematic
image using schemdraw.

Supported elements
------------------
  V<name>  <n+> <n-> DC <val>   - Voltage source
  R<name>  <n+> <n-> <val>      - Resistor
  D<name>  <n+> <n-> <model>    - Diode / LED  (with .model ... D)

Usage
-----
  python spice_to_schematic.py <netlist.spice> [<output.png>]

  If <output.png> is omitted the image is saved as schematic.png next to the
  netlist file.

Examples
--------
  python spice_to_schematic.py test.spice
  python spice_to_schematic.py test2.spice schematics/test2.png
"""

import re
import sys
import os
import math
import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use("Agg")          # headless – no display required


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _strip_comment(line: str) -> str:
    """Remove semicolons and everything after them (SPICE inline comment)."""
    return re.split(r";", line)[0].strip()


def parse_spice(path: str) -> dict:
    """Return a dict with lists 'vsources', 'resistors', 'diodes', 'models'."""
    vsources, resistors, diodes, models = [], [], [], {}

    with open(path) as fh:
        for raw in fh:
            line = _strip_comment(raw)
            if not line or line.startswith("*"):
                continue

            upper = line.upper()

            # .model  <name>  D ...
            if upper.startswith(".MODEL"):
                parts = line.split()
                if len(parts) >= 3 and parts[2].upper().startswith("D"):
                    models[parts[1].upper()] = parts[1]
                continue

            if upper.startswith(".") or upper.startswith("#"):
                continue

            parts = line.split()
            prefix = upper[0]

            if prefix == "V" and len(parts) >= 4:
                # Vname n+ n- [DC] value
                val_parts = parts[3:]
                val = val_parts[-1].rstrip("Vv")  # strip trailing V
                vsources.append({"name": parts[0], "np": parts[1], "nm": parts[2], "val": val})

            elif prefix == "R" and len(parts) >= 4:
                resistors.append({"name": parts[0], "np": parts[1], "nm": parts[2], "val": parts[3]})

            elif prefix == "D" and len(parts) >= 4:
                model_key = parts[3].upper()
                is_led = model_key in models or "LED" in model_key
                diodes.append({"name": parts[0], "np": parts[1], "nm": parts[2],
                               "model": parts[3], "is_led": is_led})

    return {"vsources": vsources, "resistors": resistors, "diodes": diodes, "models": models}


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
#
# Simple sequential layout:
#   • Voltage source(s) drawn vertically on the left rail.
#   • Each branch (R → D series pair) drawn rightward then down to ground.
#   • Ground wire connects back to the negative terminal of the source(s).
#
# Works well for the canonical LED test circuits in this project.

def draw_schematic(netlist: dict, title: str, out_path: str) -> None:
    vs = netlist["vsources"]
    rs = netlist["resistors"]
    ds = netlist["diodes"]

    # Pair each resistor with the diode it feeds (matching intermediate node)
    def find_diode_for_resistor(r):
        for d in ds:
            if d["np"] == r["nm"]:
                return d
        return None

    branches = []
    for r in rs:
        d = find_diode_for_resistor(r)
        branches.append((r, d))

    n_branches = len(branches)
    branch_width = 4.0   # horizontal spacing between branches

    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=11)

        # ------------------------------------------------------------------ #
        # Left rail – one voltage source per source in netlist (usually one)  #
        # ------------------------------------------------------------------ #
        source_top_xy = (0, 0)

        for vi, vsrc in enumerate(vs):
            label = f"{vsrc['name']}\n{vsrc['val']} V"
            src_elm = d.add(elm.SourceV().up().label(label, loc="left"))
            if vi == 0:
                source_top_xy = src_elm.end   # top-left corner

        # Top horizontal rail from source top to rightmost branch
        total_width = branch_width * n_branches
        top_rail = d.add(elm.Line().right(total_width))

        # ------------------------------------------------------------------ #
        # Branches                                                             #
        # ------------------------------------------------------------------ #
        for i, (r, diode) in enumerate(branches):
            # Drop from top rail at each branch point
            x_offset = -(n_branches - 1 - i) * branch_width

            # Tap off the top rail at appropriate fraction
            tap_x = source_top_xy[0] + branch_width * (i + 1)
            tap_y = source_top_xy[1] + d.unit  # top rail y-level

            d.add(elm.Dot(open=False).at((tap_x, tap_y)))

            # ---- Resistor going down ----
            r_label = f"{r['name']}\n{r['val']} Ω"
            res_elm = d.add(
                elm.Resistor().down().label(r_label, loc="right")
                              .at((tap_x, tap_y))
            )

            # ---- Diode / LED ----
            if diode is not None:
                d_label = diode["name"]
                elm_cls = elm.LED if diode["is_led"] else elm.Diode
                diode_elm = d.add(elm_cls().down().label(d_label, loc="right"))
                bottom_xy = diode_elm.end
            else:
                bottom_xy = res_elm.end

            # ---- Drop to ground ----
            gnd = d.add(elm.Ground().at(bottom_xy))

        # ------------------------------------------------------------------ #
        # Bottom ground rail back to source negative                          #
        # ------------------------------------------------------------------ #
        # The source negative terminal is at (0,0) after .up()
        source_neg_xy = (0, 0)
        bottom_y = bottom_xy[1]   # y of last branch ground

        d.add(elm.Line().left(total_width).at((source_top_xy[0] + total_width, bottom_y)))

        # Title
        d.add(elm.Label().at((total_width / 2, bottom_y - 0.6)).label(title, loc="right"))

        d.save(out_path, dpi=150)
        print(f"Schematic saved → {out_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    spice_path = sys.argv[1]
    if not os.path.isfile(spice_path):
        print(f"Error: file not found: {spice_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        out_path = os.path.join(os.path.dirname(os.path.abspath(spice_path)), "schematic.png")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    netlist = parse_spice(spice_path)
    title = os.path.basename(spice_path)
    draw_schematic(netlist, title, out_path)


if __name__ == "__main__":
    main()
