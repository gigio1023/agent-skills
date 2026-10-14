# Evidence and PoC

Reproduction is where a report is accepted or closed. Receivers close reports they cannot reproduce, reports that only describe a possibility from reading code, and reports whose PoC proves something other than the claim (`chromium-vrp-faq`, `apple-guidelines`, `kernel-policy`, `reddit-survey`).

## Contents

- Reproduction requirements
- Forms that experts use
- Controls
- Setup and attack kept apart
- Success and failure signals
- Minimal and harmless PoCs
- Environment capture
- Code references and quotes
- Source-only and probabilistic findings
- Attachments, names, and hashes
- Redaction
- Recordings

## Reproduction requirements

A reader with no context must be able to trigger the issue and confirm that it happened (`kernel-policy`, `google-reproduce`, `openssf-finder`). That needs the environment, the steps in order, the exact input, the expected result if the system were correct, the observed result, and where every dynamic value such as an ID or token comes from (`msrc-example`, `h1-quality`, `apple-guidelines`, `reddit-survey`). Replay your own steps from the written text before sending; omissions show up immediately (`google-reproduce`).

Keep it as short as the bug allows. A reflected issue may need one URL; a multi-party flaw needs each party's actions in order (`google-reproduce`, `google-attack-scenario`).

## Forms that experts use

| Form | When it fits | Exemplars |
| --- | --- | --- |
| Numbered steps with expected and observed results | Interactive or UI flows, short web bugs | `h1-quality`, `apple-guidelines`, `msrc-example`, `h1-gitlab-file-read` |
| Request and response pairs | HTTP and RPC boundaries; show headers that matter and the credential used | `ghsl-advisories`, `ghsa-vllm` |
| One shell block from download to result | Libraries and CLIs; include the checksum of the source tarball | `curl-h1-uaf` |
| One script that prints a clear verdict | Anything automatable; take credentials and targets as parameters | `google-automated-poc`, `ghsa-fedify` |
| Container or compose environment | Multi-service setups such as a proxy in front of a server | `h1-node-smuggling`, `curl-h1-uaf` |
| Transcript with prompts | Local privilege issues and shells | `oss-suse-screen`, `qualys-snap-confine` |
| Attempts and timing statistics | Races and probabilistic bugs where a working exploit is withheld | `oss-qualys-regresshion`, `oss-suse-screen` |

Prefer core libraries and common languages, run on a stock Linux, and avoid browser automation unless the bug requires a browser (`google-automated-poc`, `chromium-vrp-faq`).

## Controls

A control shows that the boundary normally holds, so the observed effect can only come from the flaw.

- **Baseline:** the protected action is refused through the normal path before the attack is shown (`h1-node-smuggling`, `ghsa-vllm`).
- **Negative:** no credential and a wrong credential are rejected on the same build (`local`).
- **Positive:** a correctly privileged identity succeeds, which shows the setup is working and separates the flaw from a broken environment (`local`).
- **Fixed build:** the same steps against the patched build are refused, when a patch exists (`ghsa-vllm`, `bmo-webgl`).
- **Causal:** vary one input and show the effect follows it, as Project Zero did by controlling input bytes (`p0-report-2026`).

For an authorization flaw, use two separate identities or objects so the crossing is visible (`reddit-survey`, weak). Record each control's output in its own attachment (`local`).

## Setup and attack kept apart

A PoC that creates the condition it then observes proves nothing; neither does one where the flaw lies in the PoC's own misuse of the project (`reddit-survey`, `larson-slop-2024`). Write setup steps, such as creating a second ordinary account through the normal signup page, separately from attack steps that use only what the attacker holds. Say which identity performs each step. If setup uses an administrative shortcut, say why it is equivalent to the normal path (`local`).

## Success and failure signals

A script or step that prints a verdict decides it from a signal only the flaw can produce: a state change such as a row count or a marker file, a log line printed only when the protected code runs, or a controlled read or write (`h1-node-smuggling`, `ghsa-mlflow`, `chromium-vrp-faq`). A generic error, timeout, or exception is not evidence that the attack was blocked or that it succeeded; classify it as inconclusive and show its output (`local`). Do not add decorative success messages to the target's code (`chromium-vrp-faq`). Report the exit status and the raw output beside the verdict.

## Minimal and harmless PoCs

Include only what demonstrates the issue: write a marker file rather than run a payload, read a harmless file rather than secrets, and confirm a database name rather than dump data (`ghsa-mlflow`, `bugcrowd-guide`, `node-security`). Remove harmful payloads, run with the network disabled when the bug allows it, test only systems you own or are authorized to test, and stop at accidental access to anyone else's data (`node-security`, `ghsa-mlflow`). If impact can only be analyzed by attacking real users, describe it instead and say why (`local`).

## Environment capture

Record what someone needs to rebuild the same conditions: OS and version, architecture, runtime and its version, package version and commit, container image tag and digest, build flags, relevant configuration, and the exact command line (`ghsa-mlflow`, `msrc-example`, `chromium-vrp-faq`, `django-policy`, `h1-gitlab-file-read`). Say how each value was captured, for example from the host or from the operator's notes, when it matters (`local`).

## Code references and quotes

Pin every code reference to a release tag or commit with file and line range, and quote the lines exactly, marking any omitted lines (`h1-curl-socks5`, `oss-suse-screen`, `p0-report-2026`, `local`). Show the sibling path that does have the check when one exists; the contrast makes the flaw visible without a long argument (`p0-report-2026`, `ghsl-advisories`). Quote documentation, error strings, and guards as the project wrote them. Code excerpts can carry numbered markers that the prose refers to (`talos-report`).

## Source-only and probabilistic findings

Static analysis without a demonstration is closed as not reproducible by large programs (`chromium-vrp-faq`, `apple-guidelines`). If a path could not be executed, say so in the same sentence as the claim, such as source-verified at a named commit, not run, and name any environment where it did not reproduce (`ghsa-nginx-ui`, `p0-report-2022`). If a reproducer cannot be produced at all, question the finding before reporting it (`kernel-policy`). For races, give the attempt count, success rate, and conditions, and keep the environment for re-runs (`oss-qualys-regresshion`, `oss-suse-screen`).

## Attachments, names, and hashes

- Give each file a stable descriptive name and cite that name from the observation it supports; list all files once at the end with what each one shows (`ghsa-mlflow`, `p0-report-2026`, `local`).
- Attach, do not link to a hosted copy (`chromium-vrp-faq`, `apple-guidelines`).
- Follow the venue's packaging rule: individual files named as the program asks, or an archive with a manifest, or plain text without attachments (`chromium-vrp-faq`, `curl-h1-uaf`, `kernel-policy`).
- Record the SHA-256 of every file or archive you send, and send the bytes that were reviewed; after any edit, rebuild and re-hash (`local`). `python3 -I scripts/check_report.py <report> --evidence <path> --hash` prints the hashes after the findings.
- A patch is a git patch against the stated base commit, named as a proposal (`chromium-vrp-faq`, `openssf-finder`).
- Leave out of the main bundle anything about a separate finding (`django-policy`, `local`).

## Redaction

Before sending, remove or replace home directory paths, user and host names, internal addresses, access tokens, cookies, keys, other users' data, and anything identifying an unrelated system (`ghsa-mlflow`, `node-security`, `local`). Tokens in logs and transcripts are the common miss. Run `python3 -I scripts/check_report.py <report> --evidence <dir>`; it scans text files, UTF-16 and UTF-32 files with a byte-order mark, and the members of `.zip`, `.gz`, `.tar`, `.tar.gz`, and `.tgz` archives nested up to three levels, reading up to 20 MB of each. It lists `bzip2`, `xz`, `7z`, `rar`, and `zstd` archives and hidden entries such as `.env` or `.git` as skipped without reading them, and reports an unreadable or encrypted member as `scan-error`. Token values are masked in its output. A clean scan is not proof; read the files, and open by hand anything the coverage summary lists as skipped, partial, or error. Replace a value with a labeled placeholder rather than deleting the line, so the reader still sees its shape.

## Recordings

A short unedited video helps when the flaw is visual or the receiver asks, and some triagers ask for one to filter out reports that cannot be shown (`apple-guidelines`, `chromium-vrp-faq`, `reddit-survey`). It supports the written steps and never replaces them (`cert-credibility`). Keep it short and follow the venue on hosting: Chromium wants it uploaded to the report, while Google's VRP accepts an unlisted or private link (`chromium-vrp-faq`, `google-automated-poc`). If no recording exists, do not imply one; offer to make it, and keep the environment so you can (`local`).
