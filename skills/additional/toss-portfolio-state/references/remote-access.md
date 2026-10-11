# Home-server remote access

Use this route when Toss accepts API calls only from a registered home public IP. The client device reaches a dedicated home-server runner over Tailscale SSH; it does not become an HTTP proxy, SOCKS proxy, exit node, or public service.

## One-time setup per client device

Resolve the active skill directory, then run:

```bash
bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts setup \
  --host <tailscale-dns-name-or-ip> \
  --user <ssh-user>
```

The command:

- creates a device-specific Ed25519 key if one does not exist;
- writes a managed `toss-home-api` block under `~/.ssh/config.d/` and ensures the main SSH config includes that directory;
- authorizes the public key through `ssh-copy-id`, which may request the server password once;
- deploys the bundled Bun transport and snapshot scripts to the home server;
- writes connection metadata to `~/.config/toss-portfolio-state/remote.json` with mode `600`.

If an existing SSH target can already reach the same server without a password, avoid a password prompt by adding `--bootstrap-host <existing-ssh-target>`. Each device should have its own key. Do not copy a private key between devices.

Run setup only when the user asks for or approves this local SSH configuration change. Re-run it after this skill's remote scripts change so the server copy stays aligned.

## Fetch

After setup, run:

```bash
bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts fetch \
  --market-context basic \
  --orders-days 30 \
  --recent-orders-limit 40
```

The client encodes the allowed fetch arguments and sends them to a fixed remote runner. The remote process injects its protected Toss env file and runs the bundled fetcher with Bun. The route blocks `--env-file`, `--base-url`, and `--allow-custom-base-url` so a client cannot redirect server credentials.

## Server prerequisites and failure behavior

The home server must already have:

- Bun at `~/.bun/bin/bun`;
- Toss credentials at `~/.config/toss-invest/openapi.env` with no group or other permissions;
- outbound HTTPS access to the official Toss Invest OpenAPI host.

The setup command never copies credentials from the client. If the server, Tailscale, SSH authentication, Bun runtime, or remote env file is unavailable, return a blocker. Never fall back to a client-local Toss request because its public IP may not be registered.
