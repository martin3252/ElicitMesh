# Feedback to diagram revisions

For actual user or expert feedback, record:

1. Diagram and contract version reviewed.
2. Affected node, edge, input, output, or owner.
3. Reviewer role and identity only when known and permitted.
4. Exact correction from authorized supplied material.
5. Proposed change and unresolved disagreements.
6. Scope, explicit approval status, and date.

If feedback introduces a new artifact whose meaning or supplier is unclear, follow `input-discovery.md` first: ask what it is, then who provides it, one unanswered question at a time. Logging a new mention does not justify adding a receive/read/extract path. Route unanswered domain questions to the appropriate collaborator; keep the current understood flow and use unresolved placeholders if a diagram is requested.

For clarified changes, update `workflow.yaml` and `io-contract.yaml` together, regenerate `workflow.md`, and rerun structural validation. Preserve stable IDs and record changes rather than silently replacing review history.

A correction to a diagram does not automatically approve other nodes or become a general professional quality rule. This version focuses on the diagram and I/O specification; reusable rule extraction and final domain-document generation are outside scope.
