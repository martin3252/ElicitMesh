# Example: AI engineer + lawyer (illustrative)

**Goal:** Build a candidate workflow for producing a lawyer-reviewable draft, with explicit inputs, outputs, responsibilities and pending quality requirements.

**Status:** All rules and nodes are unapproved illustrative candidates. No attorney has reviewed this repository's example. This example is not a current legal guide, not a determination of eligibility, and not a ready-to-file document.

## Starting sources

The user-provided URLs are:

- https://www.fairwork.gov.au/ending-employment/help-with-termination/unfair-dismissal#applying-for-unfair-dismissal
- https://www.fwc.gov.au/job-loss-or-dismissal/unfair-dismissal/process-unfair-dismissal-claims

The sources are listed for a real deployment to **retrieve and verify**. Their current contents, form versions, mandatory fields and filing requirements have **not** been validated as part of this sample. The sample workflow is a proposed software process, not an authoritative description of FWC proceedings.

Run `python scripts/validate_spec.py examples/legal-unfair-dismissal` from repository root after installing `PyYAML`.
