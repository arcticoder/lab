# KB: the JLC account, its coupons, and reading its quotes

Audience: future LLM sessions. The user orders PCBs, assembled boards, 3D prints, CNC parts and fasteners from JLC (JLCPCB, JLC3DP, JLCCNC, JLCMC) from Canada; prices on the account are in CAD. Facts here were observed by the user or read
from their captures; the experiment-specific plan is in `spurious-force-balance` (`docs/fabrication.md`, `docs/kb/fab_ordering_notes.md`).

## What a session can and cannot see

- The quote pages (cart.jlcpcb.com/quote, jlc3dp.com, jlccnc.com) are scripts: a fetch returns only a file-upload box and "Calculated Price $0.00". The user's captures of the option lists are `docs/jlc/pcba_quote_ui.md` (Standard PCB/PCBA) and
  `docs/jlc/3dp_quote_ui.md`; the CNC sheet-metal and HDI captures were requested and not yet made (note: the captured page lists ENIG as the default surface finish; the user reports HASL with lead is).
- The `jlc` CLI (`npm @jlcpcb/cli` 0.5.0) searches the LCSC/EasyEDA parts catalogue (stock, price, basic/extended, Economic/Standard PCBA): it has no PCB, CNC or shipping quote. Use it for parts only.
- Therefore: never state a JLC price that is not in the user's words or captures, and ask for specific numbers, not for clicking tours.

## Coupons

`docs/jlc/coupons.md` is the ledger (expiry dates, what each is for, which are maxed out or irrelevant). Rules: each coupon is used once; the terms say one coupon per order but the user reports two can be used; coupons are applied at payment and in the cart,
not in the quote lines; a coupon cannot take a line below zero (put big coupons on dear lines). Most new-user coupons end 2026-11-25 (CNC and PCB variants 11-26), others 2026-12-25. EasyEDA-design coupons need EasyEDA files. The "special offer" price of about
C$2.81 on the quote page is a new-user price for a 5-piece board up to 100 x 100 mm, not a coupon.

## Quote behaviour worth knowing

- The thickness field reverts to 1.6 mm at each upload; 1.6 mm made a 5-piece 208 x 60 mm order 0.34 kg and pushed shipping from C$2.10 to C$12.05. JLC's mass estimate is the bounding rectangle times thickness plus about 155 g of packing; the cheap tier's cliff is 0.3 kg.
- Fees seen on the 208 x 60 mm board: Engineering C$5.61, Board C$8.56, ENIG +C$25.25 (HASL C$0); quantity cannot go below 5.
- Standard PCBA needs boards of at least 70 x 70 mm with edge rails and a stencil per order; Economic is 10 x 10 mm, single side, $8 setup.
- JLCMC fasteners and the JLC3DP/JLCCNC material lists were not readable; ask the user for captures before planning with them.
