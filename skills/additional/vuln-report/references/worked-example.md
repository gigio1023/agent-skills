# Worked Example

A complete private report for GitHub private vulnerability reporting, written to the rules in this skill. Everything here is synthetic: the project `example-sitegen`, its organization, versions, commits, hashes, and the people are invented for illustration. Read it to see how the parts fit; do not copy its wording.

## Contents

- The report
- Annotations
- The same finding as a CVE description
- A variant opening

## The report

**Title:** Development server path traversal via percent-encoded dot segments in example-sitegen 2.4.1

```markdown
### Summary

The `example-sitegen serve` development server decodes percent-encoded dot segments after its `..` check, so a request for `/%2e%2e/%2e%2e/<path>` returns files outside the site directory. I read a marker file two directories above the site root on 2.4.1. The server must be reachable by the attacker, which with default settings means a local process; the documented `--host 0.0.0.0` option exposes it to the network.

### Tested version and environment

- example-sitegen 2.4.1 from PyPI, and commit `1a2b3c4d` on `main`
- CPython 3.12.6, Debian 12 container `python:3.12-slim` (digest in `env.txt`)
- Command: `example-sitegen serve ./site --host 0.0.0.0 --port 8000`

### Details

`StaticHandler.resolve()` checks for `..` in the raw request path and only then decodes it (`src/example_sitegen/serve.py` at `v2.4.1`, lines 88 to 93; line 92, a debug log call, is omitted):

    88  def resolve(self, raw_path):
    89      if ".." in raw_path.split("/"):
    90          raise NotFound()
    91      path = urllib.parse.unquote(raw_path)
        ...
    93      return open(os.path.join(self.root, path.lstrip("/")), "rb")

A segment written as `%2e%2e` passes line 89 and becomes `..` at line 91, and nothing after it checks that the joined path stays inside the root. The build command's file loader in `build.py` line 41 calls `os.path.realpath()` and rejects paths outside the root; the server path has no such check.

### Proof of concept

Setup, as the site owner:

1. `pip install example-sitegen==2.4.1`
2. `mkdir -p /tmp/t/a/site && echo MARKER-7f3a > /tmp/t/marker.txt && echo hi > /tmp/t/a/site/index.html`
3. `cd /tmp/t/a && example-sitegen serve ./site --host 0.0.0.0 --port 8000`

Attack, from another host with network access and no credentials:

    curl -s -o - -w '%{http_code}\n' 'http://<server>:8000/%2e%2e/%2e%2e/marker.txt'

Expected: `404`, as for any path outside `./site`.
Observed: `MARKER-7f3a` and `200` (`poc-encoded.txt`).

Controls on the same build:

- Literal `..` is rejected: `/../../marker.txt` returns `404` (`control-literal.txt`).
- A normal file is served: `/index.html` returns `hi` and `200` (`control-normal.txt`).

Fixed build: with the attached patch applied, the encoded request returns `404` (`fixed-encoded.txt`).

`poc.py` runs all four requests against a host given with `--target` and prints `READ`, `BLOCKED`, or `INCONCLUSIVE` for each, deciding `READ` only when the response body equals the marker.

### Impact

A client that can reach the development server reads any file the server process can read. I demonstrated this only with the marker file. The build command and the generated static output are not affected. With the default `127.0.0.1` binding, the attacker needs code running on the same machine; with `--host 0.0.0.0`, which the README recommends for previewing on a phone, anyone on the same network can read the files. I did not test whether a web page can reach the server through DNS rebinding.

### Affected versions

- Executed: 2.4.1 and commit `1a2b3c4d`.
- Source-compared, not executed: `resolve()` is unchanged from tag `v2.3.0`, where `serve` was added, through `v2.4.1`; `git log -L 88,93:src/example_sitegen/serve.py v2.3.0..v2.4.1` lists no commits.
- Earlier releases have no `serve` command.
- Proposed range: `>= 2.3.0, <= 2.4.1`; the maintainers will know the patched version.

### Suggested fix

Resolve the decoded path with `os.path.realpath()` and reject it unless it is inside the real path of the site root, as `build.py` already does. Checking for `..` after decoding would also close this request, but containment on the final path also covers symlinks. `fix-serve-containment.patch` is made against `1a2b3c4d` and adds a test for both encodings. This is a proposal; the maintainers may prefer another approach.

### Attachments

| File | Shows | SHA-256 |
| --- | --- | --- |
| `poc.py` | Runs the four requests and prints a verdict per request | `9b7e2c41...` |
| `poc-encoded.txt` | Encoded request and response on 2.4.1 | `51d0aa3e...` |
| `control-literal.txt`, `control-normal.txt` | Controls on 2.4.1 | `0c6f19b2...`, `e4a87d10...` |
| `fixed-encoded.txt` | Encoded request on the patched build | `7d2e4f90...` |
| `env.txt` | Container digest, Python and package versions | `a13c5e77...` |
| `fix-serve-containment.patch` | Proposed fix and test | `c2f0b8d5...` |

### Tooling

An AI coding assistant flagged `resolve()` during a code review I asked it to do, and drafted `poc.py`, the patch, and this report. I ran every command above on the stated environment, read the patch and the test, and checked each sentence against the outputs.

### Disclosure

I propose public disclosure when a fixed release ships or 90 days from this report, whichever comes first, and have no other time constraints. I know of no exploitation, and no one else has these details. I would like reporter credit under my GitHub account, and I can answer questions and re-run tests.
```

Form fields: ecosystem `pip`, package `example-sitegen`, affected `>= 2.3.0, <= 2.4.1`, patched left empty, severity left empty because the project's policy does not ask for one, CWE-22, AI assistance checkbox ticked.

## Annotations

- Title names component, flaw class, and condition and claims no more than was shown (`zdi-advisory`, `curl-h1-uaf`).
- The first sentence states the flaw and trigger; the second states what was demonstrated; the third states the precondition (`ghsl-advisories`, `h1-curl-socks5`, `doyensec-ovs`).
- The tested version is separate from the range, and the range is layered into executed, source-compared, and unknown (`kernel-policy`, `oss-qualys-regresshion`, `ghsa-mlflow`).
- The quote is pinned to a tag with line numbers and marks the omission; the sibling path with the check makes the flaw visible (`p0-report-2026`, `h1-curl-socks5`, `local`).
- Setup steps are the owner's, attack steps use only network access; two controls on the same build and a fixed-build run separate the flaw from the environment; each observation names its file (`h1-node-smuggling`, `ghsa-vllm`, `reddit-survey`).
- The PoC writes nothing and reads a marker file, and its verdict needs the marker in the body (`ghsa-mlflow`, `node-security`, `chromium-vrp-faq`).
- Impact states the demonstrated capability, what is not affected, the default and non-default exposure, and the one untested route, each in its own sentence (`p0-report-2026`, `cert-credibility`, `google-attack-scenario`).
- No severity, because the synthetic project's policy does not ask for one (`curl-policy`, `django-policy`).
- The fix is a proposal with a root fix and a narrower alternative, and the patch names its base commit (`p0-report-2026`, `chromium-vrp-faq`).
- The tooling paragraph says what the assistant did and what the person did, no more (`curl-ai-policy`, `github-pvr`).
- The disclosure section gives the timeline, known exploitation, who else has the details, and the credit wanted (`openssf-finder`, `cert-useful-reports`, `curl-h1-uaf`).

## The same finding as a CVE description

`Path traversal in the development server in Example Org example-sitegen 2.3.0 through 2.4.1 allows remote attackers to read arbitrary files via percent-encoded dot segments in a request path when the server listens on a non-loopback address.`

This follows the key details pattern: type, component, vendor, product, version range, attacker, impact, vector, and the condition at the end (`cve-key-details`, `cve-cna-rules`). It carries no credit and no severity.

## A variant opening

If the project had already fixed literal `..` in an earlier advisory, the summary would open with that advisory:

`GHSA-xxxx-xxxx-xxxx (fixed in 2.3.1) added a check for literal ".." segments in the development server. The check runs before percent-decoding, so "%2e%2e" segments still reach files outside the site root on 2.4.1.`

The rest follows the same skeleton, with a short section on why this is not a duplicate and a note that the maintainer chooses between a new advisory and an update (`ghsa-fedify`, `ghsa-nginx-ui`).
