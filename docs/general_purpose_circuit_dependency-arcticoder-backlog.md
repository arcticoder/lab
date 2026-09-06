# TODO: General-Purpose Circuit Build-Out — Backlog (for arcticoder)

Promote items to
[general_purpose_circuit_dependency-arcticoder.md](general_purpose_circuit_dependency-arcticoder.md)
(or
[general_purpose_circuit_dependency-arcticoder-BLOCKED.md](general_purpose_circuit_dependency-arcticoder-BLOCKED.md)
once a part gets ordered) as each becomes actionable. Nothing below has a
netlist, folder, or sourced part yet. Grouped by tier from
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md);
check the graph itself for how each node connects.

## Safety monitoring subgraph

- [ ] All 15 nodes undesigned: `LEAKDET`, `GFCI`, `ESDMON`, `INSMON`,
      `ARCDECT`, `OVERCUR`, `OVERVOLT`, `TEMPCOIL`, `EMSTOP`, `PSUHEALTH`,
      `FUSESTAT`, `RFRAD`, `VACPRES`, `SMOKDET`. (`THERM` has a part on
      order — see the BLOCKED file.)

## PSU system

- [ ] **`psu_medhigh` / `psu_high`** — no fuse/limiter circuit built
      around the Lenovo 65W adapter (on hand) or any industrial supply.

## Bootstrap tier

- [ ] `LEDIND`, `SIMPLECNT`, `TUNINGFK`, `AUDIOSC`, `CRTSC` all undesigned
      (`PASSVM` is already done via `fuse_test_voltmeter`).

## Tier 2

- [ ] `VM`, `AM`, `FREQC` undesigned as dedicated circuits (distinct from
      the bootstrap ammeter jigs).

## Tier 4

- [ ] `IA`, `DA`, `DEMOD` undesigned. (`PHASED` has a part on order — see
      the BLOCKED file.)

## Tier 6

- [ ] `LOCKIN`, `AAF`, `TIMEINT`, `JITTER` undesigned.

## Tier 9

- [ ] `SAMHOLD`, `ADCDRV`, `REFGEN2` undesigned. `MUX` is partially
      covered by `cd4066_switch_tester` component validation, but the
      actual multiplexer circuit isn't built.

## Concurrent measurement tools

- [ ] `SCOPEUSBSER`, `SCOPEDSO`, `SCOPEBENCH`, `PRECBOX`, `LOADBANK`,
      `NOISEGEN`, `TESTSIG`, `THERMOAMP` all undesigned/unsourced.
      (`SCOPELA` is the active-queue next buy.)
