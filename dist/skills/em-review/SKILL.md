---
name: em-review
description: Review and revise an ElicitMesh workflow diagram and per-node input/output contracts. Find missing fields, ambiguous branches, ownership gaps, and unsupported assumptions; incorporate actual user or expert feedback without generating final domain documents.
---

# Review and revise the diagram

Accept existing diagrams and I/O notes directly. Do not force brainstorming again or manufacture expert feedback.

Shared resources live beside this installed skill; in the source checkout use the repository root. Read `references/review-protocol.md`, `references/schema.md`, and `references/feedback-loop.md`.

1. Inspect the diagram, role map, source inventory, and contracts. Identify missing inputs, vague output formats, broken handoffs, unclear branches, and unassigned responsibility. Check each diagram node against its I/O contract.
2. Group high-impact questions by the real role who can answer them. Distinguish AI critique from expert comments. If authorized fresh-context reviewers are available, follow the shared protocol; otherwise label the critique as single-context.
3. Present findings and proposed changes. Without human feedback, leave the review pending and provide `expert-questions.md`; never simulate a lawyer or QS sign-off.
4. For actual corrections, record the exact feedback, diagram version, affected node/field, reviewer role and consented identity, and date in `review-log.yaml`. Capture disagreements and unresolved questions.
5. Revise `workflow.yaml` and `io-contract.yaml`, then regenerate `workflow.md`. Mark specific requirements approved only after an authorized person confirms their scope and version. A generic instruction to continue is not professional approval.
6. Run structural validation when possible. Deliver the revised diagram, a short change summary, and remaining questions with owners. Do not produce a final domain document or reusable quality-rule set.

Use the user's language; preserve English keys and stable IDs. Keep unverified requirements and branches visible, including when reviewer feedback is unavailable.
