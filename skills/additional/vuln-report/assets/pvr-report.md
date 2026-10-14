<!--
Skeleton for a GitHub private vulnerability report body. Replace every <...> and delete every comment.
The form's default sections are summary, details, proof of concept, and impact; keep those names if the repository uses the default form, and follow its custom form if it has one. Read the repository's SECURITY.md and reporting form first. Take conventions such as CWE choice, range syntax, and credit style from its published advisories, but not their body sections, which are often maintainer rewrites without reproduction or tested versions.
Title field: <component>: <flaw class> via <trigger> in <product> <tested version>
-->

### Summary

<!-- One to three sentences: the flaw and its trigger condition; what you demonstrated; the minimum precondition. For a variant, open with the prior advisory ID and what its fix covered. -->
<The component> <does what wrong> when <condition>, so <attacker with what access> can <demonstrated result>. I <demonstrated it how> on <version>. <Minimum precondition, and whether the default configuration is affected>.

### Tested version and environment

- <package> <version> from <source>, and commit `<sha>` on `<branch>`
- <OS, architecture, runtime and version, container image and digest>
- <exact command line or configuration used>

### Details

<!-- Root cause with file and line pinned to a tag or commit. Quote exactly; mark omitted lines. Show the sibling path that does have the check, if one exists. -->
<What the code does, in two or three sentences.> (`<path>` at `<tag>`, lines <a> to <b>):

    <exact quoted lines>

<Why this produces the flaw, and the contrast with the path that is protected.>

### Proof of concept

<!-- Setup steps use legitimate access; attack steps use only the attacker's. Name the identity for each. Every observation names the attachment that shows it. -->
Setup, as <identity>:

1. <step>
2. <step>

Attack, as <identity with only attacker access>:

    <exact request or command>

Expected: <what a correct system returns>.
Observed: <what it returned> (`<attachment>`).

Controls on the same build:

- <boundary holds through the normal path> (`<attachment>`)
- <no or wrong credential rejected> (`<attachment>`)
- <correctly privileged identity succeeds> (`<attachment>`)

Fixed build: <patched build refuses the attack, if a patch is attached> (`<attachment>`).

### Impact

<!-- Demonstrated capability first, in the present tense. Then preconditions: attacker privilege, configuration and whether it is the default, victim action, deployment. Then what is not affected. An undemonstrated chain goes in its own sentence with its condition. No severity words unless the venue asks. -->
<Attacker> can <demonstrated capability>. <Precondition list.> <What is not affected.> <If X, then Y; not demonstrated.>

### Affected versions

<!-- Optional. Include it when the venue asks for a range, such as the GitHub form's range field. The tested version above is required everywhere; a range here is your estimate for the maintainers to confirm. -->
- Executed: <versions and commits>
- Source-compared, not executed: <tags where the relevant code is unchanged, and how you checked>
- Unknown: <bound you could not establish>
- Proposed range, estimated: `>= <low>, <= <high>` <or `< <patched>` if known>

### Suggested fix

<!-- Optional. A proposal: root fix first, defense in depth second, a few sentences on how it works, the patch attached and made against the stated commit, and how the patch was tested. -->
<Root fix.> <Narrower alternative or hardening.> `<patch file>` is made against `<sha>` and <adds a test for ...>; <how you tested it>. This is a proposal; <the design choice left to the maintainers>.

### Attachments

| File | Shows | SHA-256 |
| --- | --- | --- |
| `<name>` | <what it shows> | `<hash>` |

### Tooling

<!-- What tools and AI did (found, analyzed, wrote PoC, wrote patch, drafted text) and what the person did (read, ran, verified, wrote). No stronger than what happened. Tick the form's AI checkbox if AI was used. -->
<Tool or assistant> <did what>. I <ran / read / verified what>. <Who wrote this text.>

### Disclosure

<!-- The disclosure timeline you follow or propose and any time constraints; whether you know of exploitation; who else has the details; the credit you want; that you can answer questions and re-run tests. -->
<Timeline and time constraints.> <Known exploitation, or none known.> <Who else has the details, or no one.> <Credit wanted and availability.>
