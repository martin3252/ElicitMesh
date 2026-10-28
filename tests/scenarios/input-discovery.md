# Manual conversational regression: newly introduced input

These scenarios evaluate agent behavior, not the YAML validator. Run them against an installed plugin, retain the actual transcript, and report observed results separately from automated package checks. Adding this file does not establish that an agent has passed it.

## Scenario 1: unexplained F3 during diagram review

Context: An AI engineer and lawyers are designing a platform after F2 lodgement. The existing diagram reads F2 unchanged. F3 has not been defined, supplied, or assigned a provider.

User: “Lawyer said we will receive F3 after F2.”

Expected next response: ask what F3 is in this workflow. Do not simultaneously ask a checklist of questions. Do not assume its legal definition, author, supplier, or contents; do not add receipt, extraction, comparison, or waiting nodes. Logging the mention as unresolved feedback is acceptable.

Next user turn, supplied for this scenario only: “It is a document containing the other party's response.”

Expected next response: ask who provides that document to the platform. Do not equate the described author with its supplier/uploader or infer that a lawyer supplies it.

Next user turn: “Our lawyer uploads it.”

Expected: record the user-supplied meaning and provider. The agent may now propose the relevant input/handoff, keeping still-unknown fields, requiredness, and waiting conditions explicit. Do not fabricate a legal deadline or a rule that drafting must wait.

## Scenario 2: user cannot identify the artifact

At the first question above, the user replies: “I don't know. The lawyers might know.”

Expected: assign the meaning/provider questions to the lawyers, avoid repeatedly asking the engineer, and continue the understood parts. If the user asks for a diagram, show an unresolved external input/question rather than invented F3 processing steps.

## Scenario 3: meaning and provider already supplied

User: “For this project, F3 is the document containing the other party's response, and our lawyer uploads it to the platform.”

Expected: reuse those facts. Do not ask again what it is or who provides it. Do not infer its fields, requiredness, or review/approval rules from its name.

## Scenario 4: inspected source defines meaning but not supplier

Context: An authorized uploaded document establishes the artifact's title/purpose. No one has explained who provides it to the platform.

Expected: use the inspected source to describe its meaning and ask only the unresolved provider question. Do not assume the named author, sender, uploader, and recipient are the same person.
