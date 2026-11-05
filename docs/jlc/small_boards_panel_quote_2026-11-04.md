# Quote read from the JLCONE quote page, 2026-11-04 (small-boards panel file)

Read-only via the app's debug port (recipe in `docs/kb/jlc_account_and_quotes.md`); fields changed by mouse clicks on the page, nothing saved to the cart or submitted. File: `small_panel_gerbers.zip` (36 x 96.5 mm, 2 layers, FR-4, 5 pieces, 1.2 mm, HASL with lead, green not set, 2-day build; weight 0.17 kg at 1.2 mm, 0.18 kg at 1.6 mm). Amounts C$, goods only (shipping excluded):

| Delivery Format | Different Design | Lines | Calculated |
|---|---|---|---|
| Single PCB | 1 | Special Offer C$2.79 (the normal price would be C$5.57) | **C$2.79** |
| Panel by Customer | 1 | Engineering C$5.57 + Board C$2.37 | C$7.94 |
| Panel by Customer | 2 | Engineering C$5.57 + Panel C$5.65 + Board C$2.37 | C$13.59 |
| Panel by Customer | 3 | Engineering C$5.57 + Panel C$11.31 + Board C$2.37 | C$19.25 |

So the panel fee is C$5.65 for each design beyond the first. The Special Offer needs Single PCB and does not depend on 1.2 versus 1.6 mm or on HASL; the build-time line adds C$10.59 for 24 hours (2 days is C$0). The page's default shipping line is UPS Worldwide Express Saver (C$37.41); the cheap postal tier appears at payment (the arm order paid C$1.80). The PCB coupons need goods over C$2.79, so the C$2.79 Special Offer does not qualify for them.

## The three single-board uploads (2026-11-04, later; uploaded through the app's file input, nothing saved or submitted)

Single PCB, Different Design 1, 5 pieces, FR-4, 2 layers (after each upload the page resets to 1.6 mm and OSP; thickness 1.2 mm and HASL were set by clicks on `elec_board` only). Goods, C$:

| File | Detected | Special Offer | Deburring/Edge rounding (default Yes) | Calculated |
|---|---|---|---|---|
| `clamp_plate_gerbers.zip` | 14 x 16 mm | 2.79 | 0.28 | **3.06** |
| `clamp_ground_gerbers.zip` | 19 x 17 mm | 2.79 | 0.14 | **2.92** |
| `elec_board_gerbers.zip` | 34 x 24 mm | 2.79 | 0.14 | **2.92** (weight 0.14 kg at 1.2 mm) |

The Special Offer therefore applies to every upload (confirmed). Selecting **Confirm Production file = Yes adds C$1.46** (the page raised `elec_board` from C$2.92 to C$4.39) and opens a dialog ("confirm within 48 hours or the order is confirmed automatically"; its X button cancels the choice and returns the field to No); the quotes above are with No. Shipping is not in these prices (default UPS line C$37.41; the cheap postal tier appears at payment, C$1.80 on the arm order).
