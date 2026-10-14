# Severity and Scope

Severity, weakness type, and affected range are the fields receivers most often correct. Write them as the evidence supports and leave the final call to whoever owns it.

## Contents

- Severity ownership
- Scoring only what is demonstrated
- Mitigating factors and non-vulnerabilities
- Choosing a CWE
- Determining the affected range
- Reading the target's precedent

## Severity ownership

| Venue or policy | Severity owner | What the reporter writes |
| --- | --- | --- |
| curl | The security team, four levels, no CVSS | Nothing; facts that bear on the levels (`curl-policy`, `curl-cvss`) |
| Django | The project | No CVSS, no self-assessment (`django-policy`) |
| MSRC, Chromium, Apple, Mozilla | The vendor | Facts; the vendor explains its rating (`msrc-example`, `chromium-severity`, `bmo-webgl`) |
| Project Zero tracker | The Project Zero team, which is the finder, in tracker fields | Nothing in the report body (`p0-report-2026`) |
| GitHub private reporting | Maintainer, on publication | Optional label or CVSS vector, not both (`github-pvr`) |
| HackerOne, Bugcrowd | Program triage | A field the reporter sets first (`h1-gitlab-file-read`, `curl-h1-uaf`) |
| OpenSSF guidance | Maintainer, may revise | An estimated CVSS 3.1 score with its vector and an attack scenario (`openssf-finder`, `openssf-template`) |
| ZDI, Talos, Snyk on publication | The publisher | Their own CVSS; databases can disagree with each other (`zdi-advisory`, `talos-report`, `snyk-entry`) |

CVSS measures severity, not risk; Base metrics are normally the maintainer's to set, and in CVSS 4.0 Threat and Environmental metrics belong to the consumer (`cvss31-guide`, `cvss40-spec`). The CNA rules do not require any severity (`cve-cna-rules`).

## Scoring only what is demonstrated

When the venue asks for a score, or you give an estimate where the policy is silent:

1. Choose the CVSS version the venue uses; GitHub accepts 3.1 and 4.0, and all six recent Python and agent-tooling advisories surveyed used 3.1 (`github-advisory-docs`, `ghsa-vllm`). Label 4.0 numbers CVSS-B or similar (`cvss40-spec`).
2. Score the reasonable final impact you are confident an attacker reaches, from your demonstration or from source evidence you cite (`cvss31-guide`). A metric you could not establish stays at the lower value, and the report says which metric is uncertain and why.
3. Give the full vector, not only the number, and one sentence for each metric a reader could dispute, for example why user interaction is Required or attack complexity is High (`openssf-template`, `local`).
4. Score each vulnerability on its own. A chain gets its parts' scores first and a chained score separately (`cvss31-guide`). A variant of a fixed issue is scored for its own path, not given the prior advisory's score (`local`).
5. For a library, the base score assumes the reasonable worst-case use, and the assumption is written down (`cvss31-guide`).
6. Mark the result as the reporter's estimate.

Severity words follow the score and the evidence. Words like critical in a title or summary invite a correction that costs credibility: one report claimed code execution in its title and impact line and was lowered after the maintainer listed the required conditions (`curl-h1-uaf`, `cert-credibility`). Exaggerated impact counts against a report's credibility even when the bug is real (`cert-credibility`).

## Mitigating factors and non-vulnerabilities

Receivers lower severity for unusual user interaction, no web reachability, and conditions an average user would not create; implausible interaction can make it a functional bug (`chromium-severity`). Issues that basic testing would find, or that need rare build options, rate low (`curl-policy`). Rare non-default preconditions need evidence that real deployments use them (`cert-credibility`). Say which configurations are affected and whether the default is (`oss-qualys-regresshion`, `doyensec-ovs`, `h1-curl-socks5`).

Before reporting, check the target's list of non-vulnerabilities and its threat model. Common exclusions: attacks that assume an already compromised trusted element, a local attacker who already has the access, crashes or hangs a malicious peer can cause, undocumented API misuse, debug and test code, unreleased code, and defense-in-depth gaps (`curl-policy`, `node-security`, `kernel-policy`). Chromium also excludes model output in Chrome's AI features steered by page content, unless further user harm is shown (`chromium-faq`); for LLM and agent tooling, read the target's own threat model first. A finding in these classes may still be worth a normal bug report; say which it is.

## Choosing a CWE

- Map the root cause, not the consequence: missing authorization or improper path limitation, not "authorization bypass" or "remote attacker" (`cwe-mapping`).
- Use a Base or Variant entry; use a Class only when nothing lower fits; never a Category. CWE-20, CWE-74, and CWE-284 are discouraged (`cwe-mapping`).
- Read the entry's mapping notes and check that its description matches the report's narrative. A mismatch between the weakness, the vector, and the text is a visible error; one published advisory scored no confidentiality impact while its body described a credential being sent (`ghsa-faraday`, `reddit-survey`).
- For a variant, check whether the prior advisory's CWE still describes the root cause; reuse it only if it does.
- CVE records need a weakness type, preferably a CWE (`cve-cna-rules`); GitHub advisories have been published without one (`ghsa-vllm`). Give a Base or Variant CWE when one fits.

## Determining the affected range

The tested version is required everywhere, and steps 1 and 2 cover it. Report originals mostly stopped there and left the range to the receiver (`h1-gitlab-file-read`, `curl-h1-uaf`, `ghsl-advisories`). Steps 3 to 6 apply when the venue asks for a range, such as the GitHub form's range field or the OpenSSF question list, and the result is labeled an estimate (`github-pvr`, `openssf-finder`).

1. **Tested versions.** Name every version and commit you executed the PoC on, with the environment (`ghsl-advisories`, `talos-report`, `ghsa-mlflow`).
2. **Recent code.** Confirm the issue on the development tree or latest release, at least by showing the relevant code is unchanged since the version you tested (`kernel-policy`).
3. **Source comparison.** To bound the range without running every release, compare the relevant files or functions across release tags; identical content at a tag is source evidence, not execution (`kernel-policy`, `local`). With git: `git log --oneline <tag-a>..<tag-b> -- <path>` lists commits that touched the file, `git log -L <start>,<end>:<path> <tag-a>..<tag-b>` narrows that to the lines that matter, and `git rev-parse <tag>:<path>` gives a blob ID to compare across tags. Line numbers shift between releases, so compare the function, not the number.
4. **Introducing commit.** Find where the flaw entered by bisection or by blame on the guard that is missing, and say whether earlier releases lack the feature entirely (`chromium-vrp-faq`, `oss-qualys-regresshion`, `ghsa-mlflow`).
5. **Write it in layers:** executed versions, source-compared versions, and the unknown bound, then a proposed range in the venue's syntax: `>= 2.3.0, < 2.4.2` for GitHub, `introduced` and `fixed` events for OSV, `2.3.0 through 2.4.1` or `before 2.4.2` for a CVE description (`github-advisory-docs`, `osv-schema`, `cve-key-details`).
6. **Release lines.** Give each maintained line its own range; say plainly when an end-of-life line will not be fixed (`ghsa-mcp-python-sdk`, `ghsa-asynchttpclient`).
7. **Version strings.** A build's version string may not identify its code, as when a development build still reports the last release's number. Name the commit, the tag it follows, and the first release that contains it (`local`).

Vague forms such as "latest", "all versions", or distribution-specific builds are not accepted by some receivers (`kernel-policy`, `cert-credibility`).

## Reading the target's precedent

The target's published advisories show its severity habits, CWE choices, range syntax, and credit style. Many are maintainer rewrites for users that omit reproduction, tested versions, or both, so they inform conventions rather than the report body (`ghsa-mcp-python-sdk`, `ghsa-fastmcp`). List them with the command below, or in a browser at `https://github.com/<owner>/<repo>/security/advisories`:

```bash
gh api 'repos/<owner>/<repo>/security-advisories?per_page=20' \
  --jq '.[] | [.ghsa_id, .severity, (.cvss.vector_string // ""), ([.cwes[]?.cwe_id] | join(","))] | @tsv'
```

Read the bodies of the two or three closest to your bug class. When the project has an advisory for the same component, a variant report cites it (`ghsa-fedify`, `ghsa-nginx-ui`). Precedent informs your draft; the maintainer still decides.
