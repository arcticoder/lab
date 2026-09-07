# TODO — arcticoder

Personal action items for you. Not a project/doc file, not for Claude to
work from unprompted — things only you can do (ordering, physical
verification on the bench, decisions).

> Overflow convention, only if/when this grows unwieldy (mirrors
> `aqei-bridge/docs/TODO.md`'s split, not its content or checklist detail):
> long-term/non-urgent items move to `TODO-backlog.md`, stuck items to
> `TODO-BLOCKED.md`, finished items to `TODO-completed.md`. None of those
> exist yet — don't create them until there's actually something to put in
> them.

---

## Open

- [ ] Decide whether to order the SFE Breadboard Power Supply Kit for
      `power_supplies/psu_medlow_lm317/` — currently **not ordered**
      (`power_supplies/psu_medlow_lm317/README.md`).
- [ ] With a multimeter, check whether the "TYPE-C Female Test Board"
      breakout (`pico/docs/inventory.md`) actually has CC1/CC2 pull-down
      resistors wired, before trusting `power_supplies/psu_medlow_usbc/`
      to power on from a real USB-C source. See that circuit's README
      "Status" section for what to check and why.
- [ ] If the breakout has no CC termination: either add 5.1kΩ CC1/CC2
      pull-downs yourself, source a PD sink controller IC (e.g.
      STUSB4500, CH224, TPS65987D) plus a buck converter if targeting a
      voltage other than what gets negotiated, or drop `psu_medlow_usbc`
      in favor of `psu_medlow_lm317` for that tier.
