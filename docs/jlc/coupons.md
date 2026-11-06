# JLC account coupons (user's account)

Ledger of the coupons on the JLC account. **Source of truth from 2026-11-04: the account's Unused Coupons page (`jlcpcb.com/user-center/payments/coupon`), read from the JLCONE app (15 unused coupons)**; amounts are in C$ at the current rate (US$10 = C$13.93). Rules from the coupon terms: each coupon is used once; the page terms say one coupon per order (the user earlier reported two could be used); a coupon covers the goods only ("excluding freight") and never takes a line below zero; "for orders over X" is a minimum on the goods.
A coupon's validity runs from the day "Get Coupon" is clicked (user, 2026-11-04): the coupon center (`jlcpcb.com/coupon-center`) lists unclaimed coupons with a term ("Valid for 30 / 60 days", no date) and claimed ones with "Use Now" and a date, so every dated coupon below was claimed and a coupon not yet claimed has no date: claim one only when its order is about to be placed.
The plan that assigns coupons to orders is in `spurious-force-balance/docs/fabrication.md` ("JLC orders, coupons and parcels"). Update the table when one is used.

## Unused coupons on the account (read 2026-11-04)

| Coupon | Service | Off | Minimum (goods) | Expires | Planned use |
|---|---|---|---|---|---|
| JLCONE PCB $5 | PCB | C$6.96 | over C$2.79 | 2026-11-26 | a PCB order whose goods exceed C$2.79 (the C$2.79 special offer does not qualify) |
| New User PCB - JLCPCB | PCB | C$8.36 | over C$2.79 | 2026-11-25 | same; the larger of the two |
| JLCONE 4-Layer PCB $5 | PCB | C$6.96 | over C$6.96 | 2026-12-02 | 4-layer boards only: not used (the boards are 2-layer) |
| JLCONE 6~32L PCB Coupon | PCB | C$41.78 | over C$208.92 | 2026-12-26 | not relevant |
| New User SMT - JLCPCB | PCBA | C$13.93 | over C$2.79 | 2026-11-25 | the sensor-head panel (if ordered) |
| New User PCB Stencil - JLCPCB | stencil | C$9.75 | over C$1.39 | 2026-12-25 | cannot stack with the SMT coupon in one checkout |
| JLCONE-$20 CNC Coupon | CNC | C$27.86 | over C$1.39 | 2026-11-26 | a CNC checkout |
| New User CNC - JLCCNC | CNC | C$27.86 | over C$2.79 | 2026-11-25 | first CNC checkout (aluminium arm or other part) |
| New User 3D Printing 1 - JLC3DP | 3DP | C$13.93 | over C$1.39 | 2026-11-25 | first printed-parts order |
| New User 3D Printing 2 - JLC3DP | 3DP | C$13.93 | over C$1.39 | 2026-12-25 | second printed-parts order |
| New User Mechanical Parts 1 - JLCMC | fasteners | C$13.93 | over C$1.39 | 2026-11-25 | JLCMC orders no longer combine with other services (notice 2026-11-02), so only worth it if a JLCMC line is worth its own parcel; M3 washer price unreadable (PDF catalogue pages) |
| New User Mechanical Parts 2 - JLCMC | fasteners | C$13.93 | over C$1.39 | 2026-12-25 | same; see the line above |
| New User Shipping - All Services | shipping | C$13.93 | over C$20.89 of shipping | 2026-11-25 | only above a shipping charge the plan avoids (the user's paste of 2026-11-04 read "2026/11/2", a truncation of 11/25) |
| New User Layout - JLCPCB | layout | C$27.86 | over C$1.39 | 2026-12-25 | not relevant (layout is done in KiCad) |
| New User Flex Heater - JLCPCB | flex heater | C$13.93 | over C$1.39 | 2026-12-25 | not relevant |

Used: JLCONE $8 PCB Coupon (arm order, 2026-11-04; order total C$3.00 on the account page: merchandise 1.20 + shipping 1.80), JLCCNC $10 and the Parts Special Coupons (maxed out).

## Claimable on the coupon center, not yet claimed (terms as shown 2026-11-04)

JLCONE $20 PCB (C$27.86, over C$696.40, 60 d); JLCONE Batch PCB $15 (C$20.89, over C$1392.80, 30 d); JLCONE FPC $5 (C$6.96, over C$2.79, 30 d); JLCONE High-Layer PCB $30 (C$41.78, over C$6.96, 60 d); PCB $10 and PCBA $10 - EasyEDA Design (C$13.93 each, over C$1.39, 30 d, EasyEDA files only: the EasyEDA route was dropped, so not usable); JLCONE PCBA $20 (C$27.86, over C$139.28, 30 d); JLCONE $50 PCBA (C$69.64, over C$696.40, 60 d); JLCONE Batch PCBA $30 (over C$1392.80); Stencil Coupon (C$6.96, over C$1.39, 30 d); JLCONE $20 3DP (over C$417.84, 60 d); JLCONE $20 MC (C$27.86, over C$139.28, 60 d); layout and flex-heater coupons (not relevant). The three PCB coupons above the order sizes here are out of reach (minimums of hundreds of dollars).

## 3D printing coupons that need a material or a large order (30 d unless stated; shipping over $1)

$10 Off $50 3DP Order ($10 over $50); $10 Off $40 New Materials ($10 over $40: 9000HE Resin, 3401GB Nylon, PEBA, PEEK, ABS-ESD, PLA-P, Full Color Tough Resin); $10 Essential Resin ($10 over $30: 9600, X,
9000HE, JLC Temp, JLC Black resins); $15 FDM Universal ($15 over $60: ABS, ASA, PLA, PA12-CF, TPU, PEBA, PLA-P); $10 Essential Plastics ($10 over $30: ABS, PLA-P, TPU); $30 SLA LEDO 6060 ($30 over $120);
$50 Nylon Materials Gener ($50 over $200); $25 Nylon_KeyboardPrint (60 d, $25 over $100) and $15 Nylon_KeyboardPrint (60 d, $15 over $50) for the PA nylons and 3401GB; $50 BJ 316L ($50 over $200).
The two small printed parts planned (about 25 g) will not reach these minimums; only the New User 3D Printing coupons apply.

## Not relevant to this project

JLCONE 4-Layer PCB $5 (C$6.98 off over C$6.98, 4-layer boards only, expires 2026-12-02; claimed 2026-11-04): the boards are 2-layer.
Layout service: New User Layout C$28.06, Layout $90 (90 d, over $1), JLCONE Layout $100 (over $110): the layout is done in KiCad here. 4-layer, 6-layer and high-layer PCB coupons ($5 to $42.09; JLCONE 6~32L PCB
Coupon C$42.09 over C$210.44, ends 2026-12-26): the boards are 2-layer. Flex PCB and flex heater coupons (FPC $10/$5/$15, Flex Heater $20/$20/$5/$10, New User Flex Heater C$14.03). CNC material coupons
($10 Aluminum 6061 over $100, $8 Aluminum 7075 over $100, JLCCNC $20 over $200). Mechanical-parts coupons for motors and drives ($25), transmission ($20), linear actuators ($20, $45), aluminium extrusion ($45),
aluminium enclosure ($45), pneumatics ($20, $30), linear shafts ($20). Parts Special Coupons ($5 over $60, $15 over $200; to 2036-06-02): **maxed out**.

## A coupon cannot take an order below zero

Observed 2026-10-27: with a coupon applied, a small test board's estimate fell from about C$2.00 to $0 while the "calculated price" stayed at C$2.81: the coupon covers the goods (freight is excluded) and
the unused part of it is lost. So put the large coupons on the dear lines (the arm) and the small ones on the cheap boards, and do not spend a large coupon on a line cheaper than it.

## How the quote page treats coupons (observed 2026-10-28)

The quote page says "The coupon can be applied when you select a payment method": coupons are applied at payment, not in the quote lines. The "special offer" price of about C$2.81 on the quote page is the new-user price for a
small board (5 pieces up to 100 x 100 mm), not a coupon; uploading the arm (over that size) replaced it with the normal lines (Engineering C$5.61, Board C$8.56, ENIG +C$25.25). Coupons the user could no longer select after
re-uploading may be attached to an unsubmitted order saved in the cart: deleting the saved lines in the cart is the thing to try (a guess, not confirmed). Ask JLC support if they stay locked.

## Rules the user supplied (unverified)

- Monthly SMT coupons issued at the start of a month expire at midnight on the last day of that month; claim them early.
- Exporting from EasyEDA reportedly unlocks PCBA coupons that a KiCad or Altium Gerber upload does not (the "EasyEDA Design" coupons above are that case).
- Publishing a finished project to the EasyEDA / JLCPCB Open Source Hardware Hub reportedly yields project coupons (US$10 up to US$150-400 for highlighted projects).
- Shipping coupons only apply above their shipping minimum: they do not combine with the $3-4 postal tier.
