# ElicitMesh

[English](README.md) | [繁體中文](README.zh-TW.md)

**Role-aware expert knowledge elicitation through concrete artifacts and review.**

An open-source Agent Skill that helps a builder and a domain specialist move from an incomplete explanation to a candidate workflow, input/output contracts, concrete drafts and testable acceptance rules. It **never** assumes the agent is the expert.

> Built as a standalone Skill. Inspired in part by the independent-review pattern of Google's [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model). No EGM code or reviewer prompts are bundled. Not affiliated with or endorsed by Google.

## Why this exists

A software engineer implementing a legal-document workflow may read public procedural documents, sketch the flow, then learn by presenting the flow and generated draft to a lawyer. The lawyer can identify missing input fields and output quality defects even when they cannot directly author a technical specification. This pattern also appears when a quantity surveyor and site supervisor need to clarify the scope represented by construction documents.

**ElicitMesh makes that review loop reproducible:**

1. **Role mapping:** Who are you, who are you working with, and what are you trying to deliver?
2. **Source-to-workflow:** Propose workflow steps and tag source support vs inference.
3. **I/O contracts:** Identify fields, expected outputs, quality requirements and unresolved questions.
4. **Independent critique:** Use an isolated reviewer if available; otherwise plainly label single-context critique.
5. **Artifact review:** Make a concrete sample for the actual expert to annotate.
6. **Feedback-to-rules:** Turn accepted corrections into scoped candidate rules and regression tests.

## Quick start

Use the Skill directly in a compatible agent environment by adding this directory to your environment's skill library or installing the packaged `skill.zip` through the available Skill/plugin UI. Check your host's current installation instructions; not all hosts support the same paths or invocation commands.

Example invocation:

```text
Use ElicitMesh. I am an AI/software engineer, collaborating with a lawyer
on a system that drafts unfair dismissal application documents.
Map the roles and knowledge gaps, propose a workflow with I/O contracts,
and produce a reviewable draft plus questions for the lawyer.
Treat every unknown legal requirement as pending expert confirmation.
```

Or test a second domain:

```text
Use ElicitMesh. I am a quantity surveyor working with a site supervisor.
We need a reviewable scope clarification summary. We have incomplete
BOQ/drawing revisions. Identify missing sources and who should answer.
Do not generate a site instruction.
```

If a host has no web/file access, paste authorized source excerpts or provide locally accessible documents. An unvisited URL must not be treated as reviewed evidence.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `role-map.yaml` / `.md` | Who owns information, execution, review, and approval |
| `sources.md` | Links, dates, section references, and source status |
| `workflow.yaml` / `.md` | Candidate nodes, decisions and handoffs |
| `io-contract.yaml` | Input fields, output formats, acceptance criteria |
| `expert-questions.md` | Prioritized role-specific information gaps |
| `sample-output.md` | Concrete unapproved draft for expert feedback |
| `review-log.yaml` | Actual expert comments and version references |
| `quality-rules.yaml` | Proposed and explicitly approved reusable rules |
| `acceptance-criteria.md` | Tests, review boundaries, and release blockers |

Read [references/schema.md](references/schema.md) for YAML examples.

## Validate the examples

Python 3.10+ recommended. Only `PyYAML` is required for structural validation.

```sh
python -m pip install -r requirements.txt
python scripts/validate_spec.py examples/legal-unfair-dismissal
python scripts/validate_spec.py examples/construction-scope
python -m unittest discover -s tests -v
```

These checks catch inconsistent node IDs, invalid role references, untraceable `source_supported` claims, or unsupported `approved` states. They **do not** validate legal requirements, contracts, construction safety, domain correctness, or whether a human really gave approval. Real sign-off and access control must be enforced separately in any production application.

## Optional EGM integration

EGM uses fresh-context reviewers to criticize a draft without inheriting the author's assumptions. ElicitMesh can reuse this **concept** in supported agent environments, but runs without EGM. The full EGM plugin is a separate installation. A simulated second opinion in the same chat must not be called an isolated Goldfish review.

## Privacy and safety

- Do not upload confidential legal matters, client data, or construction documents to unauthorized tools.
- Domain experts approve domain constraints; developers approve technical implementation; final release authority may be a third role.
- Do not make up mandatory fields, legal conclusions, site measurements or safety sign-offs.
- The examples use placeholders and mark professional approval as pending.
- A generated sample is not a filing-ready document or permission to conduct site work.

## License and status

Apache License 2.0. **v0.1 prototype**: a reusable instruction workflow with examples and a structural validator. It is not a hosted SaaS, professional expert system, or autonomous submission tool.

Before publishing openly, retain the license and attribution section, test on at least two different real (appropriately redacted) workflows, and ask contributors to report verified failures and expert review results rather than just generated text.
