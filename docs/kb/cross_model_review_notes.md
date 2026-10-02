# KB: cross-model review of the docs (2026-10-01)

Audience: future LLM sessions working in this repo. Not end-user content.

## What happened

The user had a second model (a fast-mode Grok) review the lab docs at
commit `6d9facd` and asked for each of its findings to be checked against
the files: agree and fix, or disagree with a counter-argument for a third
model to mediate. The user plans to use this pattern again. Expect to be
handed another model's critique; the way to handle it is below.

## How to process a critique from another model

- **Open the file before accepting or rejecting a claim.** This review's
  critique was a mix: some claims described text that isn't in the files
  (it reported stray `#` markers in the FTL doc's equations; there are none,
  and the metric and energy-density blocks are well-formed LaTeX), some
  restated things the docs already say (untested diodes, the plug-size
  unknown, the `ACTIVELIM` deferral), and some pointed at real drift.
- **A real finding is often a symptom of a different, larger one.** The
  status-drift claim was right but vague; grepping `untested|not yet` in
  `parts_reference.md`/`inventory.md`/`orders.md` found about twenty stale lines across seven parts.
  The "no quantified resolution" claim led to the Pico ADC noise-figure unit
  confusion and to the `CAPBRIDGE`/`FORCEBAL` mismatch below, neither of
  which the critique named.
- Answer in chat with per-item verdicts and reasons; file edits record the
  fix, not the debate. This file keeps the disposition so a later session
  (or the mediating model) doesn't redo the checks.
- Don't quote the user or the other model's wording into repo files.

## Dispositions

**Agreed and fixed**

| Claim | Finding | Fix |
|---|---|---|
| Status drift between `parts_reference.md` and inventory/history | Real: polyfuses, NE555, CD4066, PT334, MF52AT, TL082, SN74HC86N still said untested/not built after their bench tests; `inventory.md` PT334/MF52AT rows said TIA/THERM unassembled | Updated all, with per-unit counts ("1 of 10 exercised") |
| `SCOPELA` node stale | Real: comment said plug-in verification pending; label said 8ch while the scan reports 16ch | Label/comment rewritten; 24MHz stays "listed", max rate unmeasured |
| No quantitative resolution budget | Real gap | `spacetime_circuits_dependency.md` § Bench-scale resolution budget + `tools/resolution_budget.py` |
| No explicit scope disclaimer in the dependency docs | Partly real: force-resolution caveat existed, nothing about the FTL doc's regimes | Scope paragraph added at the top of the spacetime doc |
| Tier numbering reads as gapped | Cosmetic; the `SPACETIME` node already says 5/7/8 | One sentence added saying the interleave is deliberate |
| Citation hygiene | Tracking query strings (`utm_source=chatgpt.com`) on all reference links in the FTL doc | Stripped mechanically; no content changed |

**Disagreed (counter-arguments for the mediator)**

| Claim | Why not |
|---|---|
| FTL equations have stray `#` markers / broken line breaks | Not present. The metric and density blocks render correctly; the metric is split across lines inside one `$$` block, which is valid |
| Diode readiness implied | `inventory.md` states 18 of 20 untested and says to verify per unit |
| Cart items missing from inventory quantities | Convention: inventory tracks received parts and placed orders; carted items live in `orders.md` § In cart. Wick appears at quantity 0 on purpose |
| Resistor bin mix-up needs a kit-wide re-measure policy; 1W parts mixed with 1/4W | The caution exists, and the 1W parts are in separate tables, not the kit's |
| Track per-part cycle counts/wear | Parts are ephemeral by convention and cycle counts don't affect any planned measurement; cost outweighs value |
| CD4066 switches 2–4 are a risk | Deliberately deferred in `TODO-arcticoder.md`: validate whichever switch a build pulls. Now stated in `parts_reference.md` too |
| LM358 headroom isn't budgeted in netlists | Every LM358 netlist and README carries the Vcc−1.5V caveat, and `active_current_limiter` runs from 5V because of it |
| USB-C 5.1kΩ Rd should be measured | The board is shelved; nothing depends on it |
| 3296 "multi-turn" unverified | Already flagged unverified in three places; not a blocker for any build |
| `ACTIVELIM` requires nodes that don't exist yet | A dependency graph may point at unbuilt nodes; the deferral and its revisit trigger (`psu_medhigh` becoming a build target) are written down |
| `ACCELIF` should depend on `SCOPELA` I2C decode | `ACCELIF`'s own check reads the chip from the Pico; an analyzer decode is optional cross-checking, not a dependency |
| "Ready to build" still lists `ACCELIF` while promoting the analyzer check | `ACCELIF` is in Blocked, not Ready; only one item is startable so ranking is trivial |
| VIBISO/RIPPLETANK/safety tier have no BOM or sketch | They're Blocked/Backlog by design; designing them ahead of the actuator decision or `ACCELIF` would be against nothing |
| Single machine-readable status table | `README.md`'s bench-tested table is already the status source of truth; the fix is keeping the other three docs in step (see below) |
| 10²³ QI gap "in related repos" | Out of scope for this repo; not checked |

**Found by this review, not named in the critique**

- **`CAPBRIDGE` was documented as the no-purchase `FORCEBAL` readout.** It
  can't be: a foil plate pair is 3–90pF (`C = ε₀A/d`), `CAPBRIDGE` is
  designed for 1µF–470µF and its own README rates 10pF "No". Corrected in
  `TODO-arcticoder.md`, `TODO-agent.md` and `TODO-completed.md`;
  `history.md` is a verbatim chat log and was left alone. The purchase-free
  replacement is an optical shadow readout (LED + PT334-6C + built `TIA`),
  opened as a design item in `TODO-agent.md`.
- **The Pico ADC "noise floor <5 counts / <0.25mV" is a unit mix.**
  `read_u16()` counts are the 12-bit result ×16, so 5 counts is 0.31 of one
  real LSB. It equals the ideal quantizer's noise (LSB/√12 = 4.6 counts), so
  it is a quantization floor, not a measured resolution, and the pico repo
  states it as an expectation/sample output with no recorded bench run.
  The dependency graph's `SCOPEPICO` label and `pico/.../noise_measurement.md`
  were corrected. A real `NoiseReport` run would still be worth recording
  if someone is at the bench anyway; it isn't a to-do item on its own.
- **Dimensional nit in the FTL doc, left unedited.** The Eulerian
  energy-density expression is written with `G` but no `c`; in SI units it
  gives a mass density (the energy density is `c²` times it), while the
  metric above it uses explicit `c`. The doc calls the formula
  "schematic". It is imported source material, so flag it to the user
  instead of editing the physics; only mechanical cleanups (links) were done.

## Rule to keep status in step

After any circuit is bench-tested, run:

```bash
grep -n -i 'untested\|not yet\|designed/simulated' docs/parts_reference.md docs/inventory.md docs/orders.md
```

and update every line about that circuit's parts. `README.md`'s
bench-tested table was kept current each time; the other three files were
not, which is how about twenty lines across the three went stale. Per-unit counts ("1 of 10
exercised") are the useful form for bulk batches.
