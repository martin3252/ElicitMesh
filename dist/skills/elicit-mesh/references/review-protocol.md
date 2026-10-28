# Diagram review and optional independent critique

Review the proposed workflow and node I/O, not a generated domain document.

Check:
- Does each node have an understandable action, accountable owner, visible inputs, and named outputs?
- Can the next participant obtain the information they need? Are missing-input and decision branches explicit?
- Are field requirements, output formats, handoffs, and reviewer responsibilities known or clearly unresolved?
- Which claims have reviewed sources, which are inferred, and which need confirmation?
- Do recorded approvals apply to this exact version and scope?

Assign each finding to a real role and affected node/field. Present a short prioritized question list. Actual expert feedback belongs in `review-log.yaml`; without it, leave the review pending.

## AI critique

Use fresh-context reviewers only when available and authorized. Supply only the diagram, role map, I/O contracts, sources, and this rubric. Verify the review actually ran. Without isolation, label the result `single-context critique (not independent)`. Do not call a simulated lawyer persona professional approval.

AI critique may identify assumptions and questions. Only an authorized person can confirm domain requirements. Do not send confidential information to another service without authorization.

## EGM relationship

ElicitMesh is independent and works without Google's Elephant-Goldfish Model (https://github.com/google/elephant-goldfish-model). EGM inspired the independent-review concept. No EGM code or reviewer prompts are bundled, and compatibility with every host/version is not claimed.
