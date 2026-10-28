# Candidate workflow specification

Proposed process; domain requirements and human approval remain to be confirmed.

```mermaid
flowchart TD
    n0["collect_facts: Collect applicant-provided facts<br/>Owner: AI/software engineer<br/>Inputs: applicant_details, employment_history, dismissal_date<br/>Outputs: candidate_intake_record<br/>Evidence: inferred; approval: pending"]
    n1["specify_information: Specify information and missing fields<br/>Owner: AI/software engineer<br/>Inputs: candidate_intake_record, source_version<br/>Outputs: proposed_input_specification<br/>Evidence: inferred; approval: pending"]
    n2["review_specification: Lawyer reviews proposed information flow<br/>Owner: Lawyer<br/>Inputs: proposed_input_specification<br/>Outputs: lawyer_review_findings<br/>Evidence: inferred; approval: pending"]
    n0 -->|"Candidate intake record assembled (completeness pending review)"| n1
    n1 -->|"Proposed input specification is ready for review"| n2
    n2 -->|"Required information is missing or disputed"| n0
```

Field types, required/unknown flags, output formats, and reviewers are specified in `io-contract.yaml`.
Outputs named above describe the future process; ElicitMesh has not generated them.
