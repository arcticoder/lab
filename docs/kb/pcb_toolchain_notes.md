# KB: PCB toolchain in this repo (2026-10-22)

Audience: future LLM sessions. Facts found while setting up the fab-assembled instrument work
(`docs/research_instrument_plan.md`). User-facing setup is in `hardware/README.md`.

## What exists and what doesn't

- KiCad **9.0.9** (user installed it from the KiCad 9 PPA on 2026-10-23, replacing 7.0.11): `kicad-cli` has
  `sch erc`, `pcb drc`, `pcb render` and the exports. The symbol/footprint library packages stayed at 7.0.11.
  `pcbnew` imports under `/usr/bin/python3` (3.12), not under the
  conda Python (3.13): use `~/.venvs/lab-hw/bin/python`, a venv with `--system-site-packages`.
- No sudo from the session (a password is required), so apt installs are the user's to run.
- `pip install skidl` prints "KICADn_SYMBOL_DIR missing" warnings on import: set `KICAD7_SYMBOL_DIR=/usr/share/kicad/symbols` (and the footprint dir) before using SKiDL's KiCad library lookups.
- Freerouting 2.5.0's plain jar needs Java 25 (class file 69); the box has Java 21. The Linux release zip bundles a runtime and works headless (`-de`, `-do`, `-mp`).
- CadQuery 2.8 installs in the venv (pulls OCP); `Shape.matrixOfInertia` returns the inertia about the part's
  own centre of mass per unit density, so combine with m d² yourself (done in `balance.py`).

## Network facts

- analog.com and the Maxim mirror timed out for datasheets; ti.com, datasheets.raspberrypi.com, arxiv.org,
  github.com, jsdelivr and yaqwsx.github.io worked from curl. AliExpress pages return nothing readable.
- The JLC parts snapshot (jlcparts, `~/jlcparts/cache.sqlite3`, source-db-v2, fetched 2026-10-22) is a split
  zip: `cache.z01..z04` (50 MB each) plus `cache.zip` (10 MB). There is no `zip`/`unzip`/`7z`: concatenate
  nothing, instead read the last disk's central directory, add the sum of earlier disks' sizes to each entry's
  local-header offset (the entry carries a disk number), and inflate the deflate stream with zlib
  (`wbits=-15`). The result is one 1.6 GB sqlite file.
- Schema: `jlc_components(lcsc, category, subcategory, mfr, package, library_type, stock, price, description,
  datasheet, attributes, assembly_process, assembly_mode, ...)`. `library_type` is `base` (basic, no per-part
  setup fee) or `expand` (extended). `price` is a tier string `'1-199:0.0116,200-599:0.0092,...'`.
  **`assembly_process`/`assembly_mode` separate machine-placed parts (`SMT`/`smtWeld`, 836k rows) from
  hand-soldered through-hole parts (`THT`/`manualWeld`, 1.9M rows)**; the user's constraint is machine-placed SMT
  parts only, so every part query goes through `hardware/tools/jlc_query.py --smt`. Rows with no marking are
  basic resistors and capacitors (SMD sizes).
- The library has a category of pre-crimped leads (`Wire/Cable/DataCable`), but a fab assembles boards, not cables.

## Datasheet facts taken while selecting parts (read from the TI PDFs)

- ADS131A04 (24-bit, 4 simultaneous channels, up to 128 kSPS): AVDD 3.0 to 3.45 V with AVSS = 0 and the charge pump
  on (inputs then reach AVSS - 1.5 V), 2.442 V internal reference, 130 kΩ differential input impedance, needs a
  16.384 MHz clock or crystal; input-referred noise 5.01 µVrms at 8 kSPS gain 1 (about 79 nV/√Hz, white), 3.49 µVrms at 4 kSPS.
- LM358 (TI datasheet): the standard grade has 0.7 MHz gain-bandwidth and 0.3 V/µs slew rate; the B grade 1.2 MHz and 0.5 V/µs.
