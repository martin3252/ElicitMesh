# Expert feedback -> candidate rule -> approval -> regression test

## Minimum feedback record

For every correction capture:

1. Artifact and version: exactly what the expert saw.
2. Target: node, field, document section, or output line.
3. Reviewer role and identity when known and authorized.
4. Observed issue: what the expert actually said/changed; quote only from user-provided authorized material.
5. Proposed explanation: agent's hypothesis of why the correction matters.
6. Candidate change: input field, workflow branch, output constraint, or acceptance test.
7. Scope: project, document type, jurisdiction or business process, with version.
8. Approval state and approver: keep `pending` until explicit human confirmation.

## Translation examples (illustrative)

Expert correction: "You treated an allegation as a proven fact."

- Candidate rule: `Distinguish allegation from verified fact in every generated draft.`
- Possible new input: `fact_verification_status` (required? `unknown` pending review).
- Test: include an unverified statement in input and check that draft represents it as unverified or requests clarification.
- Expert decision: confirm exact scope and whether automated checking is sufficient.

Expert correction: "There is no drawing revision identifier."

- Candidate rule: `Show the drawing revision in this work-scope summary.`
- Possible new input: `drawing_revision`, necessity and source pending QS/authorized supervisor review.
- Test: omit revision from a sample input; system should flag it as missing rather than silently choose a version.

## Quality controls

- Distinguish a one-off editing preference from a broadly reusable rule.
- Merge semantically identical proposals; retain old versions and their origin.
- Never treat editing a document as automatically approving an extracted rule. Explicitly ask whether to adopt the rule.
- After approval, run positive, negative, and counterexample checks (where appropriate) on the next output.
- Track false positives/negatives and expert review time, not only number of extracted rules.
