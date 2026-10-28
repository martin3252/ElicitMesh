---
name: em-brainstorm
description: Explore an idea before drawing a workflow. Clarify the shared goal, collaboration roles, sources, boundaries, and unknown inputs or outputs. Use when a process is unclear or the user wants to brainstorm an ElicitMesh diagram.
---

# Brainstorm a workflow

Turn the idea into a short brief suitable for diagramming. Do not generate the final domain document or carry out the process.

Shared resources live beside this installed skill. In the source checkout, use the repository-root `references/` directory. Read `references/input-discovery.md`, `references/role-mapping.md`, and `references/domain-boundaries.md`.

1. Reuse known context. Identify the shared result, people involved, intended start and end of the process, and what is outside scope.
2. Ask only the few questions that affect the workflow: who supplies inputs, who acts, who consumes outputs, and who can resolve or approve uncertain requirements?
   When a new document or term appears, ask what it means first, then who provides it, one unanswered question at a time. Do not infer its meaning or supplier, or immediately add processing steps. If the user does not know, route the question to the right collaborator and continue the understood parts.
3. Inventory accessible authorized sources. Distinguish reviewed material, unvisited links, assumptions, and unknowns. Never infer professional requirements from intuition.
4. Compare plausible process directions and make unresolved choices visible. Keep proposals pending; agreement on a direction is not blanket expert approval.
5. Save `brief.md` with goal, scope, participants, sources, proposed steps, and prioritized questions. Add `role-map.yaml`/`.md` and `sources.md` when useful, using `references/schema.md`.

Stop after the requested brainstorming scope. Suggest `em-diagram` when the user is ready. Respond in the user's language with English machine-readable keys. Do not demand downstream files or repeat answered questions.
