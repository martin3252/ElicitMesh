# Workflow diagram schema (v0.2)

YAML describes the proposed process; `workflow.md` is its rendered view. Output names describe future deliverables, not files ElicitMesh must generate.

## Minimal diagram bundle

- `role-map.yaml` and `role-map.md`: participants, responsibilities, unresolved ownership.
- `sources.md`: actual reviewed sources, unvisited links, dates/versions where known.
- `workflow.yaml`: nodes and conditional edges.
- `io-contract.yaml`: each node's inputs and outputs.
- `workflow.md`: Mermaid diagram with action, owner, inputs, outputs, and review status inside every node.
- `expert-questions.md`: prioritized questions assigned to real roles.
- `review-log.yaml`: pending reviews or actual corrections with provenance.

Brainstorming only needs `brief.md`; do not require this complete bundle before diagramming.

## Roles

```yaml
project:
  title: Example
  goal: Agree on the information-collection workflow
  domain: example
roles:
  - id: owner
    title: Process owner (authority to confirm)
    expertise: []
    provides: [process notes]
    needs: [reviewed diagram]
    responsibilities: [clarify process]
    can_approve: []
  - id: reviewer
    title: Reviewer (identity to confirm)
    expertise: []
    provides: [corrections]
    needs: [diagram with node I/O]
    responsibilities: [review proposed handoffs]
    can_approve: []
```

Use a declared unresolved role for unknown ownership; do not fabricate approval authority.

## Nodes, edges, and contracts

A node requires `id`, `title`, `owner_role`, `evidence_status`, and `approval_status`.
An edge requires `from`, `to`, a nonempty `condition`, and both states.
Each node has exactly one contract:

```yaml
contracts:
  - node_id: collect_information
    inputs:
      - name: supplied_notes
        type: text
        required: unknown
        evidence_status: inferred
        approval_status: pending
        source_refs: []
        approver_role: reviewer
    outputs:
      - name: information_register
        format: table_to_confirm
        quality_criteria: [Show missing information explicitly]
        evidence_status: inferred
        approval_status: pending
        source_refs: []
        approver_role: reviewer
```

Inputs and outputs must be nonempty lists. If unresolved, use a named entry such as `input_to_confirm` with `type: unknown` and `required: unknown`, or `output_to_confirm` with `format: unknown`. Requirements are proposals until reviewed.

## Evidence and approval

Evidence: `source_supported | inferred | unknown`.
Approval: `pending | approved | rejected | needs_info`.
A source-supported entry needs `source_refs`. An approved entry needs `approved_by` and `approved_at`, and explicit human confirmation scoped to that version. The validator checks metadata, not whether that confirmation really happened.

## Review log

```yaml
reviews:
  - id: review-001
    target: workflow.md
    artifact_version: v1
    reviewer_role: reviewer
    reviewer_identity: null
    received_at: null
    status: pending
    feedback: []
```

Completed reviews require a consented reviewer identity and received date. Record each actual correction's node/field, original comment, proposed change, and resolution; do not fabricate reviews.

## Render and validate

```sh
python scripts/render_diagram.py <bundle-directory>
python scripts/validate_spec.py <bundle-directory>
```

The renderer places I/O inside each node and labels every edge. The validator checks role/node references, I/O coverage, provenance/approval metadata, and that the diagram matches its YAML. Regenerate after editing the YAML; keep extra commentary in the brief or questions file. Neither command validates domain accuracy.
