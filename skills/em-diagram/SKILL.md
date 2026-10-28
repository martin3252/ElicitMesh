---
name: em-diagram
description: Turn an idea, brief, or existing notes into a workflow diagram showing every node's action, owner, inputs, and outputs. Use for ElicitMesh process mapping, decisions, missing-input paths, and handoff specifications without generating final domain documents.
---

# Draw the workflow and node I/O

The diagram is the deliverable. Naming a future output does not authorize creating it or executing the workflow.

Shared resources live beside this installed skill; in the source checkout use the repository root. Read `references/input-discovery.md`, `references/schema.md`, `references/role-mapping.md`, and `references/domain-boundaries.md`.

1. Accept a brief, existing artifacts, or the user's idea directly. Reuse known roles and sources; ask only for missing information that materially prevents diagramming.
   For a newly introduced input, clarify its meaning first and its supplier next, one unanswered question at a time. Do not add receive/read/extract nodes from an unexplained document name. If the user cannot answer and wants a diagram, show an unresolved input and route the question to the relevant collaborator.
2. Propose 3–8 nodes with stable IDs, action titles, and owner roles. Represent unresolved ownership as a declared unknown role rather than pretending authority is settled.
3. For each node specify input names/documents/fields, type, whether required (`true`, `false`, or `unknown`), output names and expected formats, and the appropriate reviewer. Describe outputs; do not generate them.
4. Write `workflow.yaml` and `io-contract.yaml`. Label conditional edges, missing-information paths, and review handoffs. Do not invent legal deadlines, mandatory fields, or approval authority.
5. Show action, owner, input names, output names, and approval status inside every diagram node. Put additional detail in the contracts, not exclusively there.
6. Save `workflow.md`, role map, source inventory, `expert-questions.md`, and a pending `review-log.yaml`. Use bundled `scripts/render_diagram.py` to render Mermaid and `scripts/validate_spec.py` to validate the full bundle when Python/PyYAML are available. These checks do not establish domain correctness.

Keep evidence and approval separate. Deliver the diagram, key unknowns, and the role best placed to resolve each one. Respond in the user's language with English keys. `em-review` can revise this specification later. Do not create application drafts, work orders, or professional rule sets.
