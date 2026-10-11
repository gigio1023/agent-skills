# Throwaway Prototypes

A throwaway prototype is code written to answer one design question during exploration and then set aside. It is not a first version of the module. Build one when running something would settle the question faster than argument. When the question is how well a concept performs, it belongs to ml-experiment or evaluation-design instead: a prototype run on a handful of synthetic cases cannot carry a performance claim.

## Before building

Write the question at the top of the prototype, where a reader sees it before the code: the design question it answers and the observation that would answer it either way. Propose the prototype with that question and its rough cost unless the user has already asked for one, because it writes files and runs code.

Useful questions are behavioral. Does a scoring rule order hard synthetic cases the way the concept assumes? Does a state model reject a transition it should forbid? Does an agent loop recover after a tool call fails? Does a mechanism produce any signal on cases constructed to contain it?

## While building

- Mark it as throwaway in its name and header, and place it in a scratch or exploration location the project already uses, outside the real module's source tree.
- Never import it from the real system or wire it into one. It touches no production endpoint, shared database, real credential, or real user data. Synthetic data is labeled synthetic.
- Keep state in memory unless persistence is the question; a scratch store then gets a name that says to delete it.
- Make it run with one command, and show the full relevant state after each step so the user sees what changed.
- Skip polish: no tests, abstractions, or error handling beyond what running it needs.
- For a defensive module or an attack agent, exercise the design on synthetic cases in a local sandbox. Do not query real systems adversarially or embed concrete adversarial inputs, and keep the record in methodology language.

## After

Record the answer in the exploration record: the question, what was observed, and how it moves the concept's core bet or weakest assumption. Keep the prototype only as the source of that answer, in a throwaway location or branch when the project wants it kept. The decision moves forward through design-doc or an experiment; the real implementation is written against that decision, and the prototype code is not wired in.

## Source

These rules adapt the `prototype` skill in [mattpocock/skills at 49dd158](https://github.com/mattpocock/skills/tree/49dd158/skills/engineering/prototype) (MIT), rewritten for design exploration. This version keeps its discipline of a stated question, throwaway labeling, one-command runs, and visible state. It drops the UI-variant branch and the step that lifts validated logic into the real module, since here a prototype answers a design question and never enters the system.
