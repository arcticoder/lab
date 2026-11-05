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
not in the quote lines; a coupon cannot take a line below zero (put big coupons on dear lines). A coupon's expiry runs from the day the user clicks "Get Coupon" (reported 2026-11-04): a coupon that is not claimed yet has no date, and claiming early burns its term, so claim only when the order is about to be placed. Most new-user coupons end 2026-11-25 (CNC and PCB variants 11-26), others 2026-12-25. EasyEDA-design coupons need EasyEDA files. The "special offer" price of about
C$2.81 on the quote page is a new-user price for a 5-piece board up to 100 x 100 mm, not a coupon.

## Quote behaviour worth knowing

- The thickness field reverts to 1.6 mm at each upload; 1.6 mm made a 5-piece 208 x 60 mm order 0.34 kg and pushed shipping from C$2.10 to C$12.05. JLC's mass estimate is the bounding rectangle times thickness plus about 155 g of packing; the cheap tier's cliff is 0.3 kg.
- Fees seen on the 208 x 60 mm board: Engineering C$5.61, Board C$8.56, ENIG +C$25.25 (HASL C$0); quantity cannot go below 5.
- Standard PCBA needs boards of at least 70 x 70 mm with edge rails and a stencil per order; Economic is 10 x 10 mm, single side, $8 setup.
- JLCMC fasteners and the JLC3DP/JLCCNC material lists were not readable; ask the user for captures before planning with them.

## Reading the quote page from the JLCONE desktop app (2026-11-04, works only when the user launches it with a debug port)

`jlcone --remote-debugging-port=9222` (the user starts it; never restart or flag the app yourself) exposes Chromium's DevTools at 127.0.0.1:9222. The app keeps no quote or coupon data on disk (its profile `~/.config/jlcone` holds login state and cached scripts only; do not open the cookies). Read-only recipe, no clicks and no JLC API calls: `GET http://127.0.0.1:9222/json/list` lists the tabs (the quote page is `https://cart.jlcpcb.com/quote`, the account page `https://jlcpcb.com/user-center/`); connect to the tab's `webSocketDebuggerUrl` with `websocket.create_connection(url, suppress_origin=True)` (the browser rejects an Origin header with 403) and send `Runtime.evaluate` with `document.body.innerText` for the page text; input values (dimensions X/Y) come from `document.querySelectorAll('input')`; the selected option of a button group is the one whose computed border/background colour differs from its siblings (classes carry no "active"). The quote page shows after an upload: the detected size ("96.5x36mm" lists the long side first), the charge details (Special Offer, Calculated Price), a shipping estimate (default UPS line, far dearer than the postal tier shown at payment) and the weight. The page resets thickness to 1.6 mm and the finish to ENIG after each upload.
