# KB: power-rail budget across the designed circuits

Audience: future LLM sessions. Not end-user content (see
`repo_docs_conventions.md` for the kb/docs split).

## Why this file exists (2026-10-01)

`TODO-arcticoder.md` once carried the line that AA cells can't power this
bench, which backed buying the SparkFun LM317 kit from RobotShop. The user
questioned it, correctly: the claim was true only for `ACTIVELIM`'s 2A
check, and not enough circuits had been designed to show the rest needed
more than cells provide. A tally, per circuit, against the rails the bench
actually has:

| Circuit | Rail | Load (design or measured) | Fits AA stack / Pico 3V3? |
|---------|------|---------------------------|---------------------------|
| `psu_4xaa` (the rail itself) | 6.0V, 4 cells | under 300mA budget | is the AA rail |
| `psu_low_v2` | 3.0V, 2 cells | 253mA design point, 2.53V measured | yes, it is the AA rail |
| `transimpedance_amplifier` | `psu_low_v2` | sub-mA | yes |
| `charge_amplifier`, `electric_field_probe`, `phase_detector` | Pico 3V3 (`psu_pico_rail`) | sub-mA to a few mA | yes |
| `ne555_astable` | `psu_4xaa` (needs ≥4.5V) | milliamps | yes |
| `accelerometer_interface` | Pico 3V3 | under 5mA (GY-521, datasheet-recalled) | yes |
| `adc_ads1115` | Pico 3V3 | about 1mA incl. divider and pull-ups | yes |
| `vibration_driver` | Pico 3V3, or `psu_low_v2` | 96mA worst case (stalled-winding model) | at `psu_pico_rail`'s conservative ~100mA budget (the regulator is documented ~300mA shared, unmeasured here), so nothing else should draw from that pin; `psu_low_v2` is the roomier option |
| `inductance_bridge`, `capacitance_bridge`, `thermal_monitor` | Pico 3V3 / GPIO | milliamps | yes |
| `active_current_limiter` bench check | needs 2A | 5V into 5Ω is 1A+, the design point is a 2A trip | **no — Deferred**; no AA stack sources this |

Nothing on the list needs a regulated 3.3V/5V rail above about 300mA from
wall power, and the Pico's own USB 5V (VBUS, ~500mA shared with the Pico)
covers a servo-class load. That is why the kit was shelved: not because AA
cells are universally enough, but because no designed circuit breaks the
budget. **Revive the kit (or another wall-powered regulator) when a design
does** — a mains-fed adapter on hand (12V, ≥1A, see `orders.md`) is the
input source for it.

## Rules for future sessions

- Keep this table current when a circuit is added. A design whose load
  exceeds what its rail gives goes to `TODO-agent.md` as a rail decision,
  not as a purchase assumed in advance.
- Never write "can't be done with AA cells" in a doc without the specific
  load that breaks it; the user checks such claims against the circuit list.
- Brush noise from a motor on the Pico's 3V3 pin disturbs the Pico's ADC (its
  reference is that rail): the `vibration_driver` README says so. A design
  that needs both a motor and ADC reads at once should give the motor its
  own rail, which is a real reason to build a second AA rail, not the kit.
