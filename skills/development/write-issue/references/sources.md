# Sources

Read this when a rule in `SKILL.md` is questioned or being changed. It lists the public sources behind the rules that are not obvious, says what kind of support each one gives, and separates them from the local choices of this skill. Sources were read on 2026-09-17.

## How Strong The Support Is

Most of it is vendor opinion written for product software teams, or a methodology author's prescription from experience. Product behavior quoted from documentation is fact about that product. The two empirical studies below are a classroom experiment with student teams and an interview study of 14 organizations, and neither studied research teams. No source found addresses a lone research engineer using a product team's tracker. Treat the rules as well-motivated defaults, which is why a team's own convention wins over them.

## Public Sources

| Rule | Source | Kind of support |
| --- | --- | --- |
| An issue is one task with a clear outcome. Titles are short. The description is optional. | Linear Method, [Write issues not user stories](https://linear.app/method/write-issues-not-user-stories): "An issue should describe a task with a clear, defined outcome", and "Descriptions should be optional–not required" | Vendor opinion |
| Quote the reporter and link the conversation. | Same page: "quote user feedback directly instead of summarizing it... Link to the customer conversation" | Vendor opinion |
| Name exploratory work as a deliverable. | Same page: create a placeholder to break down later, "or frame it as a deliverable (e.g. Write project spec)" | Vendor opinion, stated for design exploration |
| No acceptance-criteria section by default. Checks live where work is reviewed. | The 77 Linear method and documentation pages reviewed never use the terms acceptance criteria or definition of done, which is silence and not a rejection. The [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) repository keeps its completion checklist in `EVALUATION_CHECKLIST.md` for pull requests, while its issue templates ask for metadata and reproduction steps. | Observation of public practice, small sample |
| A completion condition for research work, when one is required. | SAFe, [Spikes](https://framework.scaledagile.com/spikes): a spike should "develop only the necessary data to identify and size the stories that drive it" (wording from an archived 2023 copy). So the condition is "enough is known to define the next work", not "the target number was reached". | Prescription, single source |
| Results and reasoning live in an experiment log, not the tracker. One round of experiments answers one question. | [Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook): each round "should have a clear goal and be sufficiently narrow in scope", and "Untracked experiments might as well not exist." | Practitioner guidance |
| No estimates for uncertain work. | Shape Up, [Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03): "Estimates start with a design and end with a number. Appetites start with a number and end with a design." | Prescription |
| Split when the lumps have shown up, not before. | Shape Up, [Map the Scopes](https://basecamp.com/shapeup/3.3-chapter-12): "You need to walk the territory before you can draw the map." See also imagined versus discovered tasks in [Hand Over Responsibility](https://basecamp.com/shapeup/3.1-chapter-10). | Prescription |
| Keep in-progress work few. | [The Kanban Guide](https://kanbanguides.org/the-kanban-guide/2025.5/): members "must explicitly control the number of work items in a workflow" | Prescription |
| Exploratory work resists fixed task lists, and no limit at all also fails. | Saltz and Hotz 2021, [interview study](https://scholarspace.manoa.hawaii.edu/handle/10125/70728): exploration "often lacks a clear set of required tasks", yet too much freedom lets "tasks linger longer than required". Saltz, Shamshurin, and Crowston 2017, [classroom experiment](https://scholarspace.manoa.hawaii.edu/handle/10125/41273): under Scrum "task estimation was very difficult". | Empirical, weak: 14 organizations; 85 students in 16 teams |

The Linear mechanics in `linear.md` come from Linear's documentation: [parent and sub-issues](https://linear.app/docs/parent-and-sub-issues), [issue relations](https://linear.app/docs/issue-relations), [projects](https://linear.app/docs/projects), [project milestones](https://linear.app/docs/project-milestones), [project updates](https://linear.app/docs/initiative-and-project-updates), [documents](https://linear.app/docs/documents), [issue templates](https://linear.app/docs/issue-templates), and [triage](https://linear.app/docs/triage).

## Local Choices

These rules are this skill's own and have no public citation. They come from the pack owner's stated preferences and from failures observed in real use, so change them with the owner, not by appeal to a source.

- The assignee default: assign the author, leave it empty when ownership is ambiguous, and never assign another named person unasked.
- The rules under "State The Claim, Justify Every Link". They follow the reader-access principles of `share-internal-doc` in Gigio Pack and answer an observed failure: issues that pointed at paths on the author's machine or a server, and at piles of loosely related links, instead of stating their findings.
- The Korean noun-phrase outline for tracker records.
- The rules under "Tables, Figures, And Collapsed Detail": an optional overview table right after the purpose sentence with named columns and rows and short cells, a figure made with the `technical-diagram` skill when structure is the point and it is worth making, and a collapsed section only as a last resort, because a shorter issue is preferred to a folded one. The tracker forms in `linear.md` and `github-issues.md` are product facts from Linear's [editor documentation](https://linear.app/docs/editor), GitHub's [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections) and [creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) pages, and the help text of `gh` 2.101.0, all read on 2026-09-17.
