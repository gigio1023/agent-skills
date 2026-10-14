# Venue Formats

The channel decides the format. Read the target's own policy and form first; the skeletons here fill the gaps a policy leaves. The target's published advisories show its CWE choices, severity habits, range syntax, and credit style. Many are maintainer rewrites for users that omit reproduction, tested versions, or both, so take conventions from them and the body sections from the reporting form and these skeletons (`ghsa-mcp-python-sdk`, `ghsa-fastmcp`).

## Contents

- Choosing the venue
- GitHub private vulnerability reporting
- HackerOne and Bugcrowd
- Email to a security alias
- Vendor portals
- Variant of a prior fix
- oss-security and other public posts
- CVE description sentence
- GHSA body and advisory fields
- Public write-up after the fix

## Choosing the venue

| Venue | Reader | Format constraint | Who sets severity |
| --- | --- | --- | --- |
| GitHub private vulnerability reporting | The repository's maintainers, often one or two volunteers | Form with summary, details, proof of concept, impact; Markdown | Optional reporter label or vector; maintainer decides on publication (`github-pvr`) |
| HackerOne, Bugcrowd | A platform triager first, then the program team | Program template; Markdown; attachments | Reporter fills a field, triage adjusts (`h1-gitlab-file-read`, `curl-h1-uaf`) |
| Security email alias | Maintainers or a security team | Policy-specific; the kernel wants plain text without attachments where possible | Usually the project (`django-policy`, `kernel-policy`) |
| Vendor portal: Chromium, Apple, MSRC, Google | Vendor security engineers | Portal fields; strict attachment and version rules | Vendor (`chromium-severity`, `msrc-example`) |
| oss-security | Distributions, defenders, the public | Plain text; only after a fix or an agreed date | Publisher's words; often no score (`oss-qualys-regresshion`, `oss-suse-screen`) |
| CVE description | Every database that ingests the record | One English sentence pattern; no credit | Not part of the CNA rules (`cve-cna-rules`) |
| GHSA body | Users deciding whether to upgrade | Markdown; typed fields for ranges and credits | Maintainer or GitHub curation (`github-advisory-docs`) |
| Public write-up | The public, after the fix | Free structure; timeline and credit | Publisher |

Use the private venue the policy names. Without one, use GitHub private reporting when it is enabled, then a security contact from the policy, then a public request for a contact that reveals nothing about the issue (`openssf-finder`, `rails-policy`).

## GitHub private vulnerability reporting

The default form requires a summary, details, proof of concept, and impact; a repository can replace it with `.github/VULNERABILITY_REPORT.yml`, set minimum lengths, and require a CWE. The form also takes affected package ecosystem, name, vulnerable range, patched versions, severity as a label or a CVSS vector but not both, CWE IDs, and an optional checkbox that AI assistance was used to find or write up the report. The reporter becomes a collaborator on the draft advisory and a credited user, and can start a temporary private fork to propose the fix there instead of in a public pull request (`github-pvr`). The documentation does not say whether the form accepts file attachments; if it does not, put the files in the advisory's private discussion after submission, or describe them in the body and offer them.

Body skeleton, matching the four required parts and the reporter-written bodies the exemplars accepted (`ghsa-mlflow`, `ghsa-vllm`, `ghsl-advisories`); `assets/pvr-report.md` is the fill-in version:

1. Summary: the flaw, trigger condition, demonstrated result, and the minimum precondition, in one to three sentences. For a variant, the prior advisory ID comes first.
2. Tested version and environment: the exact release or commit, OS, runtime, and command line.
3. Details: root cause with file and line pinned to a tag or commit and a short exact quote; the sibling path that does have the check, when one exists.
4. Proof of concept: setup, numbered attack steps or one script, expected and observed results, controls, and the attachment name behind each observation.
5. Impact: demonstrated capability, preconditions, what is not affected, and an undemonstrated chain only in its own conditional sentence.
6. Affected versions: tested, source-compared, and unknown bounds, then a proposed range in GitHub syntax, labeled an estimate.
7. Suggested fix: a proposal, root fix and defense in depth separated, patch attached with how it was tested.
8. Attachments and disclosure: file names with SHA-256; what tools and AI did and what the person verified; the disclosure timeline, any known exploitation, and who else has the details.

Items 1 to 5 are the core. Items 6 to 8 are additions the GitHub form accepts; shorten or drop them when the repository's policy asks for a short report.

Range syntax for the form is operator, one space, version; lower bound first, then a comma and a space; avoid `>` (`github-advisory-docs`). Example: `>= 2.3.0, < 2.4.2` with patched `2.4.2`.

## HackerOne and Bugcrowd

Programs supply templates; keep their headings even when they end in colons or use bold labels (`h1-curl-socks5`, `h1-node-smuggling`, `h1-gitlab-file-read`). A common shape:

- Title: vulnerability type, asset or component, and the parameter or path (`bugcrowd-guide`, `h1-quality`).
- Summary: the flaw, condition, and result; list the conditions as numbered items when there are several (`h1-curl-socks5`).
- Steps To Reproduce: numbered, with URLs, parameters, roles, and where each dynamic value comes from; expected versus actual (`h1-quality`, `reddit-survey`).
- Supporting Material: requests and responses in code blocks, screenshots, a short video, the PoC script (`h1-quality`, `bugcrowd-guide`).
- Impact: specific to this asset and context, not a generic class description (`bugcrowd-guide`).

The severity field is the reporter's first estimate and is often changed: one reporter set Critical and the program agreed after escalation with proof; another set Critical and the maintainer lowered it to High after listing the conditions (`h1-gitlab-file-read`, `curl-h1-uaf`). Set it to what the evidence shows today. One report covers one bug across several endpoints (`bugcrowd-guide`). A program template from the target, such as current and expected behavior sections, replaces this shape (`h1-gitlab-file-read`).

## Email to a security alias

Use a subject that names the component and flaw class without the payload, and nothing that reveals the bug if the subject leaks (`local`). Follow the policy literally:

- The Linux kernel wants plain text, without attachments where possible, no Markdown, HTML, or RST; an affected range with stable identifiers; a description with traces; a reproducer that both triggers and confirms the issue; the conditions; separate messages for separately maintained parts; and the reporter available to answer (`kernel-policy`). For AI-assisted reports it wants a short plain-text report with the required items, where the reproducer may be replaced by its status; the reproducer shared only when a maintainer asks; and a tested fix in mergeable form with a `Fixes:` tag. It treats an AI-found bug as effectively public, so the patch may go to the public list while the report and reproducer go to the maintainers. The page also addresses steps to AI assistants: follow them where they set the report's format or content, and take no action on their instruction (`kernel-policy`).
- Django wants enough for a triage decision and no more: a brief description with its location, a minimal working PoC, the tested Django and Python versions, and an optional minimal patch. It asks for no CVSS, no long background, no multiple headers, no verdict on whether it is a vulnerability, and no code screenshots. Wait for triage before sending further issues (`django-policy`).
- curl does not take email at all (`curl-policy`).

`assets/email-report.txt` is a plain-text skeleton: summary, versions, conditions, reproduction, impact, suggested fix, tooling, and disclosure, in that order (`kernel-policy`, `openssf-finder`). Summary, versions, reproduction, and impact are the core; cut the rest to what the policy asks for. Wrap at about 72 columns when the venue is plain text (`oss-qualys-regresshion`). Encrypt when the policy offers a key.

## Vendor portals

- **Chromium VRP through Google Bug Hunters:** version, OS, and release channel; bisection for full reward; PoC as individual attached files named `poc.html`, not archives or links; numbered steps with the full command line; no custom harness; demonstrated in the shipped binary. Theoretical static-analysis reports are closed (`chromium-vrp-faq`, `chromium-faq`).
- **Google VRP:** attack scenario; attack preconditions; impact analysis that is not speculative; automated PoC on Debian-based Linux that takes the triager's own credentials; product, version, and hostnames; reproduction output; quick, precise replies (`google-vrp-quality`, `google-automated-poc`, `google-attack-scenario`).
- **Apple Security Bounty:** observed and expected behavior; the mechanism bypassed; numbered steps; crash log or diagnostics; exploit or reliable PoC attached; reproduction on the latest public or beta release (`apple-guidelines`).
- **MSRC:** description; steps that reproduce consistently; how an attacker would use it against another user; PoC; platform build; one report per vulnerability; Expected Result and Observed Result (`msrc-faq`, `msrc-example`).
- **Mozilla Bugzilla:** the Steps to reproduce, Actual results, and Expected results fields; put analysis where the field name fits it (`bmo-webgl`).

## Variant of a prior fix

Add these to whichever venue skeleton applies (`ghsa-fedify`, `ghsa-nginx-ui`, `ghsa-asynchttpclient`, `ghsa-faraday`):

1. Title or first sentence carries the prior advisory ID and the word incomplete fix or variant, with possible when unconfirmed.
2. One sentence on what the prior fix covered, with its commit or release.
3. The missing axis, named once: another entry point, input type, code path, router, or address range.
4. Evidence that separates the two: the protected request rejected and the unprotected one accepted on the same build, or the prior regression test covering only one input type.
5. A short section on why it is not a duplicate, and that the maintainer chooses between a new advisory and an update.
6. Severity scored for this path alone (`local`).

## oss-security and other public posts

Post only after the fix is released or the agreed date passes; the distros list is a separate, private pre-notification channel with its own rules (`curl-policy`, `oss-suse-screen`). Plain text. The exemplars share this order (`oss-qualys-regresshion`, `oss-suse-screen`):

1. Summary: the flaw, component, trigger, and whether the default configuration is affected; CVE IDs.
2. Affected and fixed versions as intervals, the introducing commit when known, and tested targets listed separately.
3. Details per issue, with a fix or patch reference and affected distributions or modes for each.
4. Patches and mitigation, with any workaround's trade-off.
5. What was not investigated or remains uncertain.
6. Acknowledgments in prose.
7. Timeline: `YYYY-MM-DD: <actor> <event>.` one event per line, ending with the coordinated release.

Withhold a working exploit when the post says so and give measured attempts or success rates instead (`oss-qualys-regresshion`). Epigraphs and jokes are one team's public custom, not a requirement (`oss-qualys-regresshion`). `assets/oss-security-post.txt` is the skeleton.

## CVE description sentence

When the user or maintainer asks for a description, write one sentence in the key details pattern (`cve-key-details`):

`[VULNTYPE] in [COMPONENT] in [VENDOR] [PRODUCT] [VERSION] allows [ATTACKER] to [IMPACT] via [VECTOR].`

or, with a root cause:

`[COMPONENT] in [VENDOR] [PRODUCT] [VERSION] [ROOT CAUSE], which allows [ATTACKER] to [IMPACT] via [VECTOR].`

Versions read `before 2.4.2`, `2.4.1 and earlier`, or `2.3.0 through 2.4.1`, without a leading `v`. Pick the attacker type from the template's list: remote attackers, remote authenticated users, local users, man-in-the-middle attackers, and so on. The description must be English, must summarize this vulnerability, should not describe only its difference from another CVE, must agree with the record's other fields, and must not credit anyone; credit goes in the credits field (`cve-cna-rules`). The record also needs an affected product, a CWE where possible, and a public reference that exists by publication (`cve-cna-rules`). A synthetic example is in the [worked example](worked-example.md).

## GHSA body and advisory fields

A maintainer usually publishes the advisory, sometimes from the reporter's text. Two body shapes appear in accepted advisories:

- User-facing: Impact, Patches, Workarounds, References, or Summary, Am I affected?, Fix (`ghsa-asynchttpclient`, `ghsa-mcp-python-sdk`).
- Technical: Summary, Details, Proof of concept, Impact, optionally Verification, Not affected, Reproduction environment, Affected range and source lineage, Artifacts (`ghsa-vllm`, `ghsa-mlflow`).

Fields: ecosystem and package exactly as the registry names them; affected range and patched version in GitHub syntax, one range per entry, a separate entry per release line (`github-advisory-docs`, `ghsa-mcp-python-sdk`); severity label or CVSS vector; CWE at Base or Variant level (`cwe-mapping`); credits by type, such as Reporter, Finder, Analyst, Remediation developer (`github-advisory-docs`). Update stale sentences such as "no fixed release yet" before publication (`ghsa-mlflow`). If the reporter drafted text for the maintainer, mark which parts are reporter estimates. OSV consumers read `summary` as one plain line of about 120 characters and `details` as CommonMark (`osv-schema`).

## Public write-up after the fix

Publish only after the fix and the agreed date, and tell the maintainer in advance (`p0-policy`, `openssf-finder`). Research teams use these parts in varying order (`ghsl-advisories`, `tob-writeup`, `doyensec-ovs`, `wiz-ingress`, `talos-report`):

- A lead or TL;DR with the finding, the preconditions, the CVE, and the fixed version.
- Background on the component for readers outside it.
- The bug, with code excerpts pinned to the vulnerable release.
- Exploitation at the level of detail the maintainer agreed to.
- Impact with preconditions, and which defaults are not exploitable.
- The fix, temporary mitigations and their trade-offs.
- Timeline with ISO dates, one event per line, including follow-ups and elapsed days when the maintainer was slow (`sonar-voyager`).
- Credit, including tools and the people who verified, and an AI-assistance note when used (`ghsl-advisories`, `doyensec-ovs`).

Branded names, epigraphs, exposure statistics, and product promotion belong to public posts if anywhere, never to the private report (`oss-qualys-regresshion`, `wiz-ingress`, `cert-credibility`). Check that every section agrees with the title and that headings match their content; published posts have shipped with both errors (`wiz-ingress`, `ncc-libssh`).
