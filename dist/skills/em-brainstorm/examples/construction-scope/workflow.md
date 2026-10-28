# Candidate workflow specification

Proposed process; domain requirements and human approval remain to be confirmed.

```mermaid
flowchart TD
    n0["collect_scope_sources: Collect drawings and BOQ references<br/>Owner: Quantity surveyor<br/>Inputs: drawing_reference, boq_item_reference<br/>Outputs: source_register<br/>Evidence: inferred; approval: pending"]
    n1["map_scope_gaps: Identify scope information and gaps<br/>Owner: Quantity surveyor<br/>Inputs: source_register<br/>Outputs: scope_information_gaps<br/>Evidence: inferred; approval: pending"]
    n2["review_site_clarity: Site supervisor checks scope clarity and identifies issues<br/>Owner: Site supervisor<br/>Inputs: scope_information_gaps<br/>Outputs: clarification_list<br/>Evidence: inferred; approval: pending"]
    n0 -->|"Documents and revisions identified or explicitly marked missing"| n1
    n1 -->|"Proposed information gaps are ready for discussion"| n2
    n2 -->|"Sources or revisions are missing or conflicting"| n0
```

Field types, required/unknown flags, output formats, and reviewers are specified in `io-contract.yaml`.
Outputs named above describe the future process; ElicitMesh has not generated them.
