# KB: cross-repo docs conventions

Audience: future LLM sessions working in this repo (or the sibling `pico/`
repo). Process/structural notes about how the docs here are organized —
not useful to the end user, who already knows this stuff first-hand.

## `spacetime_circuits_dependency.md` is pure mermaid, no prose

The entire file is a single mermaid `graph TD` block — there is no prose
legend or explanatory section before/after it. Every node's documentation
*is* its bracketed label text (e.g. `PASSVM["..."]`), and edges are
explained only by inline `%%` comments grouped just above blocks of edges.
Consequence: when a node's real-world implementation changes (e.g. it
turns out to be already satisfied by an existing circuit, or a planned
approach is dropped in favor of another), the fix is to edit the label
text in place — there's no separate paragraph elsewhere to update, and
none should be added (would duplicate/drift from the label). Example:
`PASSVM` was originally labeled "Passive Analog Voltmeter with
Galvanometer"; updated 2026-08-21 to reflect that the Pico-ADC-as-voltmeter
approach (already implemented in `fuse_test_voltmeter/` and used in both
`psu_ultralow_v1`/`psu_low_v2` READMEs' "Validation without a multimeter"
sections) replaces the galvanometer build entirely — no separate circuit
needs to be designed for this bootstrap node.

## README cross-linking is one-directional: `lab/` → `pico/`, never back

`lab/README.md` is the workspace-home README (the `lab.code-workspace` file
opens both `../pico` and `.`, with `lab/` as the primary folder). Per
explicit user instruction, when `lab/` docs need to reference Pico
usage/setup that's already fully documented in `pico/README.md` (e.g. the
WSL `usbipd` device-attach dance, MicroPython firmware flashing,
`mpremote` install/usage), link out to the relevant `pico/README.md`
section instead of copying the steps. Do not add a reverse link from
`pico/README.md` back to `lab/README.md` — `pico/` is meant to stand alone
as the general-purpose Pico repo and shouldn't need to know about the
lab-specific consumer of its instructions. If `pico/README.md`'s section
headings change, re-check the anchor links from `lab/README.md` (currently
`../pico/README.md#running-on-real-hardware`).
