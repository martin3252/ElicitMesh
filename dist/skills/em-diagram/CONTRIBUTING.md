# Contributing to ElicitMesh

Contributions are welcome if they improve the safety, clarity or portability of the role-aware specification workflow.

## Before submitting a change

1. Include a minimal redacted or synthetic input and expected output.
2. Explain which failure mode it addresses (role ambiguity, missing node I/O, source provenance, review authority, or unclear branches).
3. Run `python -m unittest discover -s tests -v` and validate `examples/legal-unfair-dismissal`, the AI engineer–lawyer example. Additional domain examples should wait until they can be reviewed.
4. Do not commit real client data, actual legal advice to a named person, private drawings, credentials, or privileged documents.
5. Never add a blanket instruction to accept AI review as professional approval.

Questions and proposed domain templates should identify the intended role with review authority and applicable jurisdiction, standard or project scope. Domain templates without reviewed evidence must be marked as experimental.

This repository is independent from Google EGM; references to EGM are conceptual and not an assertion of compatibility with every version or agent runtime.
