# Independent review / optional EGM integration

The independent review should challenge the draft, NOT merely rewrite the same model's answer in a skeptical tone. An authentic Goldfish review requires a fresh context without access to the parent conversation or assumptions. The reviewer should receive only source material, the specific draft/spec, the role map, and this rubric. A second prompt in the same conversation is **not isolated**.

## Generic independent-review prompt

> Read the supplied source excerpts, role map, workflow, I/O contracts and sample output as a reviewer with no prior discussion history. Identify every unsupported assertion, missing input, ambiguous output criterion, unassigned approval, conflicting definition and unhandled exception that could block safe implementation. For each finding, return severity (blocker/major/minor), affected node/field, evidence, question, and best real-world role to ask. Do not invent domain rules and do not approve anything.

## Optional review lenses

- Source Goldfish: missing provenance, unsupported inferences, outdated source versions.
- I/O Goldfish: undefined fields, missing file format, unclear error/empty-state behavior.
- Fresh-reader Goldfish: jargon, implicit assumptions, ambiguous participant terminology.
- Domain-question Goldfish: generate questions appropriate for a qualified expert, but NOT simulated legal/engineering/safety sign-off.
- Regression Goldfish: old expert corrections missing from new output.

## Runtime behavior

- If independent subagent tools are present, start a genuinely fresh context and include explicit material. Verify the review actually ran.
- If absent, label output `single-context critique (not independent)`; do not call it Goldfish.
- Do not send privileged data to a different provider or tool without authorization.
- Always assign final approval to an authorized person, not an AI persona.

## Elephant-Goldfish Model relationship

ElicitMesh was designed to be **standalone**. It may work alongside the EGM plugin, whose source is at https://github.com/google/elephant-goldfish-model and is distributed under Apache-2.0. This project does not bundle EGM code or prompts. Do not assume EGM commands, reviewers, or file layout are installed. When installed and supported, EGM can help review technical specs, but does not validate domain correctness or replace a real expert.
