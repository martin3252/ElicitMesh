# ElicitMesh artifact schemas (v0.1)

Treat YAML as canonical; Markdown is a human-readable view. Use empty arrays / `null` for missing knowledge, not invented facts. The validator checks structural invariants, not professional correctness.

## role-map.yaml

```yaml
project:
  title: Example project
  goal: A concrete shared deliverable
  domain: legal-tech
roles:
  - id: engineer
    title: Software engineer
    expertise: [software systems]
    provides: [technical implementation]
    needs: [domain constraints]
    responsibilities: [workflow implementation]
    can_approve: [technical behavior]
  - id: expert
    title: Domain expert
    expertise: [domain rules]
    provides: [reviewed sample corrections]
    needs: [reviewable sample]
    responsibilities: [domain quality review]
    can_approve: [specified domain content]
```

## workflow.yaml

```yaml
nodes:
  - id: collect_input
    title: Collect input
    owner_role: engineer
    evidence_status: inferred
    approval_status: pending
    source_refs: []
  - id: create_draft
    title: Draft output
    owner_role: engineer
    evidence_status: inferred
    approval_status: pending
    source_refs: []
edges:
  - from: collect_input
    to: create_draft
    condition: Input ready
    evidence_status: inferred
    approval_status: pending
```

## io-contract.yaml

```yaml
contracts:
  - node_id: collect_input
    inputs:
      - name: case_facts
        type: text
        required: unknown
        evidence_status: inferred
        approval_status: pending
        source_refs: []
        approver_role: expert
    outputs:
      - name: intake_record
        format: structured_data
        quality_criteria: [Record received facts verbatim]
        evidence_status: inferred
        approval_status: pending
        source_refs: []
        approver_role: expert
```

`required` is `true`, `false`, or `unknown`; unknown is strongly preferred to guessing. `format` is the expected presentation or data format, not necessarily a software schema.

## review-log.yaml

```yaml
reviews:
  - id: review-001
    target: sample-output.md
    reviewer_role: expert
    reviewer_identity: null
    received_at: null
    status: pending
    feedback: []
```

Only store reviewer identity with consent. A pending review placeholder is not evidence of review.

## quality-rules.yaml

```yaml
rules:
  - id: q001
    statement: Date references must be consistent within this draft
    scope: this document type in this project
    originating_feedback: null
    evidence_status: inferred
    approval_status: pending
    approved_by: null
    approved_at: null
    approver_role: expert
    check_type: deterministic
    test_case: Compare relevant date fields for inconsistencies
```

Approved rules require `approved_by`, `approved_at`, and `originating_feedback` or `source_refs`. If approval scope changes, downgrade to `pending` until re-approved.

## Provenance model

Use two independent axes:

- Evidence: `source_supported | inferred | unknown`
- Approval: `pending | approved | rejected | needs_info`

`source_supported` is not the same as `approved`; an official source may describe a process yet leave implementation questions unanswered. `approved` is not the same as `true` across all domains; it must be scoped to one artifact, rule, jurisdiction, project, or version.
