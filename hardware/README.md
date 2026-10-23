# hardware/ — the force balance and its fab-assembled electronics

The plan is in [docs/research_instrument_plan.md](../docs/research_instrument_plan.md); the task list is
[docs/TODO-agent.md](../docs/TODO-agent.md) Part A.

| Folder | Contents |
|--------|----------|
| `balance/` | The torsion balance: `params.py` (single source of numbers), `model.py` (analytic model), `balance.py` (CadQuery CAD, exports `cad/*.stl` and `balance.step`), `render.py` (PNG views), `smoke_test.py` |
| `tools/` | `jlc_query.py`: search the JLCPCB parts library snapshot for stock, price, basic/extended and whether a part is machine-placed |
| `instrument/` | The fab-assembled electronics: requirements, parts, schematic (in progress) |

`tools/force_noise_budget.py` (top-level `tools/`) is the force-noise prediction (gate G3).

## Toolchain (set up 2026-10-22; nothing here is in the repo's git history except the scripts)

| Piece | Where | How it got there |
|-------|-------|------------------|
| KiCad 9.0.9 and `kicad-cli` | `/usr/bin` | installed by the user from the KiCad 9 PPA on 2026-10-23; the CLI has `sch erc`, `pcb drc`, `pcb render` and the Gerber/drill/BOM exports. The symbol and footprint library packages are still 7.0.11 |
| Python environment | `~/.venvs/lab-hw` | `/usr/bin/python3 -m venv --system-site-packages ~/.venvs/lab-hw`; the system site packages carry `pcbnew` (KiCad's Python module, version 9.0.9 since the upgrade) |
| `skidl`, `kiutils`, `easyeda2kicad`, `cadquery`, `numpy`, `scipy`, `matplotlib` | the venv | `~/.venvs/lab-hw/bin/pip install skidl kiutils easyeda2kicad cadquery numpy scipy matplotlib` |
| Freerouting 2.5.0 (autorouter) | `~/tools/freerouting/freerouting-2.5.0-linux-x64/bin/freerouting` | the release zip (it bundles its own Java 25 runtime; the system's Java 21 can't run the plain jar). Headless: `-de in.dsn -do out.ses -mp 20` |
| JLC parts snapshot | `~/jlcparts/cache.sqlite3` (1.6 GB) | `https://yaqwsx.github.io/jlcparts/data/cache.z01 .. cache.z04` and `cache.zip` (a split zip with no `unzip` available: reassemble with a short Python script that adds each disk's offset, see `docs/kb/pcb_toolchain_notes.md`). Refresh before an order: stock and prices are a daily snapshot |
| ngspice | `/usr/bin/ngspice` | already installed; used for every analog block |

Run the CAD and the combined smoke test with the venv's Python:
`~/.venvs/lab-hw/bin/python hardware/balance/smoke_test.py` (with the system Python the CAD checks
are skipped, not failed).

**Electrical and design rules checks.** `kicad-cli sch erc` and `kicad-cli pcb drc` run from the command line (KiCad 9.0.9); `kicad-cli pcb render` gives the images for the WP6 visual review.
