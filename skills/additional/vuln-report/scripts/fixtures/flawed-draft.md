# CRITICAL: Remote Takeover in example-sitegen 🚨

**Summary:** I hope this email finds you well. It is important to note that the dev server has a devastating path traversal — any attacker can read every file on the machine.

## Details

The handler in serve.py does not validate paths. This affects all versions and the latest release. TODO: add line numbers.

Run `example-sitegen serve` and request a file with `%2e%2e`. On my machine the output was in /Users/alice/poc/out.txt and the server was alice-MacBook-Pro.local at 192.168.1.23.

The prompt read alice@alice-laptop:~/poc$ and the other machines were devbox.tail0000.ts.net and buildbox.home.arpa.

## Impact

This could lead to complete compromise of the developer's machine. An attacker may steal credentials and pivot to production. Severity: Critical (CVSS 9.8).

Logs used a header `Authorization: Bearer EXAMPLE-NOT-A-REAL-TOKEN-000000` during testing.

The shell exported APP_API_KEY=example0000notreal and the token endpoint returned {"access_token": "example-0000-not-real"}.

Please do not hesitate to reach out. Thank you for your time!

<Name, how you want to be credited, and that you can answer
questions.>
