# Role mapping protocol

Identify collaboration participants by what they **actually do**, not what the agent guesses their job title implies.

## Required fields

- `project.goal`: concrete shared result, ideally a reviewable artifact.
- `roles[].id`: stable machine identifier.
- `roles[].title`: title given by user or `unknown`.
- `roles[].expertise`: domain expertise or technical expertise demonstrated/confirmed.
- `roles[].provides`: what information or artifacts the role can provide.
- `roles[].needs`: what the role needs from others.
- `roles[].responsibilities`: work they own.
- `roles[].can_approve`: exact deliverables/decisions they can approve, or empty if unclear.

## Process

1. Build role pairs or a small role network. User can be an engineer, expert, PM, translator, reviewer, customer, or all of them.
2. Identify collaboration outcome, available sources, and the actual decision maker.
3. For each interface between roles, write: `Role A has -> Role B needs -> why needed -> proof of acceptance`.
4. Classify gaps: fact not provided, interpretation undecided, input schema unclear, output quality ambiguous, ownership missing, or conflicting terminology.
5. Route each clarification question to the person with relevant expertise and authority, not merely to the first available person.
6. For a role-only user request, present matrix and 3-7 prioritized questions; do not infer full legal/building specifications.

## Approval authority

Distinguish `provider`, `executor`, `technical_reviewer`, `domain_reviewer`, and `final_approver`. These may be the same individual, but never assume that. A lawyer may approve legal requirements but not database architecture. Final release authority may belong to a product owner rather than either the lawyer or the engineer.
