# JLC account coupons (user's account, prices in CAD)

Ledger of the coupons on the JLC account, read from the account page on 2026-10-27. C$1.399 = US$1 (C$13.99 = US$10). One coupon applies per checkout, so each coupon needs
its own order. Dates marked "?" are not shown in the list the user pasted: the user reads them off the account (spurious-force-balance `docs/TODO-arcticoder.md`). The plan
that assigns coupons to orders is in spurious-force-balance `docs/fabrication.md` ("JLC orders, coupons and parcels"). Update the Status column when a coupon is used.

## New-user coupons (dated)

| Coupon | Service | Off (C$ / US$) | Minimum | Excludes | Expires | Status | Planned use |
|---|---|---|---|---|---|---|---|
| New User PCB | JLCPCB bare boards | 8.40 / 6.00 | C$2.80 | freight | 2026-11-25 | unused | mechanical boards order |
| New User SMT | JLCPCB assembly | 13.99 / 10 | C$2.80 | freight | 2026-11-25 | unused | early sensor-head PCBA (Part N), else lapses |
| New User PCB Stencil | JLCPCB stencil | 9.80 / 7.00 | C$1.40 | | 2026-12-25 | unused | cannot stack with the SMT coupon in one checkout: only for a later PCBA order that also needs a stencil |
| New User Layout | JLCPCB layout service | 27.99 / 20 | C$1.40 | | 2026-12-25 | unused | not planned (layout is done in KiCad here) |
| New User Flex Heater | JLCPCB flex heater | 13.99 / 10 | C$1.40 | | 2026-12-25 | unused | not planned; a flex heater could serve thermal-control tests (backlog idea) |
| New User CNC | JLCCNC | 27.99 / 20 | C$2.80 | freight | 2026-11-25 | unused | a CNC part if Part K finds one worth it (an aluminium arm is the candidate) |
| New User 3D Printing 1 | JLC3DP | 13.99 / 10 | C$1.40 | | 2026-11-25 | unused | first printed-parts order |
| New User 3D Printing 2 | JLC3DP | 13.99 / 10 | C$1.40 | | 2026-12-25 | unused | second printed-parts order |
| New User Mechanical Parts 1 | JLCMC | 13.99 / 10 | C$1.40 | | 2026-11-25 | unused | M3 stainless nuts and washers if listed |
| New User Mechanical Parts 2 | JLCMC | 13.99 / 10 | C$1.40 | | 2026-12-25 | unused | second fastener order if needed |
| New User Shipping - All Services | any | 13.99 / 10 | C$20.99 of shipping | | 2026-11-25 | unused | only useful on a parcel whose shipping exceeds C$20.99: the plan avoids those |

## Promotional coupons (30 or 60 days from issue; exact dates "?")

| Coupon | Service | Off (C$) | Minimum (C$, excl. freight) | Eligible products | Expires | Status |
|---|---|---|---|---|---|---|
| $10 Off $50 3DP Order | JLC3DP | 13.99 | 69.97 | any 3DP | ? (30 d) | unused |
| $10 Off $40 New Materials | JLC3DP | 13.99 | 55.97 | 9000HE Resin, 3401GB Nylon, PEBA, PEEK, ABS-ESD, PLA-P, Full Color Tough Resin | ? (30 d) | unused |
| $10 Off $40 - Global Ship | shipping | 13.99 | 55.97 of shipping | any | ? (30 d) | unused |
| $10 Essential Resin | JLC3DP | 13.99 | 41.98 | 9600, X, 9000HE, JLC Temp, JLC Black resins | ? (30 d) | unused |
| $15 FDM Universal | JLC3DP | 20.99 | 83.96 | ABS, ASA, PLA, PA12-CF, TPU, PEBA, PLA-P | ? (30 d) | unused |
| $10 Essential Plastics | JLC3DP | 13.99 | 41.98 | ABS, PLA-P, TPU | ? (30 d) | unused |
| $30 SLA LEDO 6060 Resin | JLC3DP | 41.98 | 167.92 | LEDO 6060 Resin | ? (30 d) | unused |
| $25 Nylon_KeyboardPrint | JLC3DP | 34.98 | 139.93 | PA12-HP, PAC-HP, 3201PA-F, 1172Pro, 3301PA, PA11-HP, PA12S-HP, 3401GB nylons | ? (60 d) | unused |
| $15 Nylon_KeyboardPrint | JLC3DP | 20.99 | 69.97 | the same nylons | ? (60 d) | unused |

All the promotional printing coupons also state "shipping over C$1.40" (a condition on the order).

## Rules (user-supplied unless marked; verify at checkout)

- One coupon per checkout (order batch). Unused coupons stay until their own expiry.
- Monthly SMT coupons issued at the start of a month expire at midnight on the last day of that month; claim them early.
- Exporting from EasyEDA reportedly unlocks PCBA coupons that a KiCad or Altium Gerber upload does not. Unverified.
- Publishing a finished project to the EasyEDA / JLCPCB Open Source Hardware Hub reportedly yields project coupons (US$10 up to US$150-400 for highlighted projects). Unverified.
- Shipping coupons only apply above their shipping minimum (C$20.99 all services, C$55.97 global ship): they do not combine with the $3-4 postal tier.
