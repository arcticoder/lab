# JLC account coupons (user's account)

Ledger of the coupons on the JLC account, from the lists the user pasted on 2026-10-27 (the second list, of the new-user coupons, replaced the first: their amounts had shifted with the exchange rate,
C$14.03 = US$10 now). Rules from the account page's terms: each coupon can be used once, and **only one coupon can be applied to any order**; JLCPCB can change or cancel a coupon at any time; coupons are valid
in certain regions only (all of these show for the user's account). "Excl. freight" = the minimum is on the goods. Amounts without a currency prefix are exactly as pasted (they read as US$; verify at checkout).
Expiry: a date when the page gives one; "30 d" and "60 d" coupons have no date in the paste (the user reads it off the account: `spurious-force-balance/docs/TODO-arcticoder.md`). The plan that assigns coupons to
orders is in `spurious-force-balance/docs/fabrication.md` ("JLC orders, coupons and parcels"). Update Status when one is used.

## Used for the plan (PCB, PCBA, stencil, CNC, 3D printing, mechanical parts)

| Coupon | Service | Off | Minimum | Conditions | Expires | Planned use |
|---|---|---|---|---|---|---|
| JLCONE $8 PCB Coupon | PCB | C$11.22 | C$14.03 | shipping over C$0.70 | 2026-11-26 | **the mechanical boards order** (larger than New User PCB) |
| New User PCB - JLCPCB | PCB | C$8.42 | C$2.81 | | 2026-11-25 | a second PCB checkout, if any (see "cart lines" below) |
| PCB $10 - EasyEDA Design | PCB | $10.00 | $1 | EasyEDA files only | 30 d | not usable with KiCad Gerbers |
| JLCONE PCB $5 | PCB | $5.00 | $2 | shipping over $1 | 30 d | alternative to New User PCB |
| New User SMT - JLCPCB | PCBA | C$14.03 | C$2.81 | | 2026-11-25 | **sensor-head panel** (if ordered) |
| PCBA Special Offer | PCBA | $9.00 | $1 | expires in 3 days (about 2026-10-30) | ~2026-10-30 | only if the panel is ordered within days; the New User SMT coupon is larger and lasts longer |
| PCBA Special Offer | PCBA | $6.00 | $1 | expires in 3 days | ~2026-10-30 | |
| PCBA $10 - EasyEDA Design (two entries) | PCBA | $10.00 | $1 | EasyEDA files only | 30 d | not usable with KiCad outputs |
| JLCONE PCBA $20 | PCBA | $20.00 | $100 | | 30 d | the electronics order, if it is dated in time (it will not be) |
| New User PCB Stencil - JLCPCB | stencil | C$9.82 | C$1.40 | | 2026-12-25 | cannot stack with the SMT coupon in one checkout |
| Stencil Coupon | stencil | $5.00 | $1 | | 30 d | |
| New User CNC - JLCCNC | CNC | C$28.06 | C$2.81 | | 2026-11-25 | first CNC checkout (aluminium arm or other part) |
| JLCONE-$20 CNC Coupon | CNC | C$28.06 | C$1.40 | shipping over C$0.70 | 2026-11-26 | a second CNC checkout |
| JLCCNC $10 Coupon | CNC | $10.00 | $1 | | 2035-07-31 | **maxed out** |
| New User 3D Printing 1 - JLC3DP | 3DP | C$14.03 | C$1.40 | | 2026-11-25 | first printed-parts order |
| New User 3D Printing 2 - JLC3DP | 3DP | C$14.03 | C$1.40 | | 2026-12-25 | second printed-parts order |
| New User Mechanical Parts 1 / 2 - JLCMC | fasteners | C$14.03 each | C$1.40 | | 2026-11-25 / 12-25 | M3 stainless nuts and washers, if listed |
| New User Shipping - All Services | shipping | C$14.03 | C$21.04 of shipping | | 2026-11-25 | only above a shipping charge the plan avoids |
| $10 Off $40 - Global Ship | shipping | $10.00 | $40 of shipping | | 30 d | same |

## 3D printing coupons that need a material or a large order (30 d unless stated; shipping over $1)

$10 Off $50 3DP Order ($10 over $50); $10 Off $40 New Materials ($10 over $40: 9000HE Resin, 3401GB Nylon, PEBA, PEEK, ABS-ESD, PLA-P, Full Color Tough Resin); $10 Essential Resin ($10 over $30: 9600, X,
9000HE, JLC Temp, JLC Black resins); $15 FDM Universal ($15 over $60: ABS, ASA, PLA, PA12-CF, TPU, PEBA, PLA-P); $10 Essential Plastics ($10 over $30: ABS, PLA-P, TPU); $30 SLA LEDO 6060 ($30 over $120);
$50 Nylon Materials Gener ($50 over $200); $25 Nylon_KeyboardPrint (60 d, $25 over $100) and $15 Nylon_KeyboardPrint (60 d, $15 over $50) for the PA nylons and 3401GB; $50 BJ 316L ($50 over $200).
The two small printed parts planned (about 25 g) will not reach these minimums; only the New User 3D Printing coupons apply.

## Not relevant to this project

Layout service: New User Layout C$28.06, Layout $90 (90 d, over $1), JLCONE Layout $100 (over $110): the layout is done in KiCad here. 4-layer, 6-layer and high-layer PCB coupons ($5 to $42.09; JLCONE 6~32L PCB
Coupon C$42.09 over C$210.44, ends 2026-12-26): the boards are 2-layer. Flex PCB and flex heater coupons (FPC $10/$5/$15, Flex Heater $20/$20/$5/$10, New User Flex Heater C$14.03). CNC material coupons
($10 Aluminum 6061 over $100, $8 Aluminum 7075 over $100, JLCCNC $20 over $200). Mechanical-parts coupons for motors and drives ($25), transmission ($20), linear actuators ($20, $45), aluminium extrusion ($45),
aluminium enclosure ($45), pneumatics ($20, $30), linear shafts ($20). Parts Special Coupons ($5 over $60, $15 over $200; to 2036-06-02): **maxed out**.

## A coupon cannot take an order below zero

Observed 2026-10-27: with a coupon applied, a small test board's estimate fell from about C$2.00 to $0 while the "calculated price" stayed at C$2.81: the coupon covers the goods (freight is excluded) and
the unused part of it is lost. So put the large coupons on the dear lines (the arm) and the small ones on the cheap boards, and do not spend a large coupon on a line cheaper than it.

## Cart lines

Each uploaded design is a cart line. The terms say one coupon per order; whether each cart line counts as its own order (so the four mechanical boards could take up to four coupons, e.g. JLCONE $8 PCB, New User PCB,
JLCONE PCB $5 and another) is unknown: the user can see it in the cart (apply a coupon to one line, then try another on a second line) and report it in `TODO-arcticoder.md`.

## Rules the user supplied (unverified)

- Monthly SMT coupons issued at the start of a month expire at midnight on the last day of that month; claim them early.
- Exporting from EasyEDA reportedly unlocks PCBA coupons that a KiCad or Altium Gerber upload does not (the "EasyEDA Design" coupons above are that case).
- Publishing a finished project to the EasyEDA / JLCPCB Open Source Hardware Hub reportedly yields project coupons (US$10 up to US$150-400 for highlighted projects).
- Shipping coupons only apply above their shipping minimum: they do not combine with the $3-4 postal tier.
