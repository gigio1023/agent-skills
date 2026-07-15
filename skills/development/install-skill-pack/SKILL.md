---
name: install-skill-pack
description: >
  Use when installing or refreshing the published `gigio1023/agent-skills` pack
  globally for explicitly selected agents after changes reach `main`, or when
  updating already tracked global skills on request. Resolves the latest Skills
  CLI once per run, reviews partner security audits before global installation,
  and verifies discovery. NOT for local checkouts, PR branches, commit SHAs,
  project-local installs, pre-merge testing, unscoped all-agent installs, or
  silently changing unrelated global skills.
---

# Install Skill Pack

Install only the published `main` branch of `gigio1023/agent-skills`. Let the
Skills CLI manage destinations for the agents named by the user. Never
substitute a newer local checkout or PR ref.

## Quick Path

1. Resolve an explicit list of target agent IDs from the user's request or the
   current harness. Do not widen it to every CLI-supported agent.

2. Execute the bundled installer from this skill directory, passing each target
   agent explicitly:

   ```bash
   bash scripts/install_latest_pack.sh \
     --agent <target-agent-id> \
     --agent <another-target-agent-id>
   ```

   The script resolves npm's current `skills@latest` version once, verifies the
   reported CLI version, and reuses that exact version for both phases. It first
   performs a disposable project-scope install with a temporary npm cache so
   agent auto-detection cannot mutate the real global install before review.

3. Review the complete `Security Risk Assessments` table from the disposable
   preflight before answering the script's confirmation:

   - Cancel on any Gen high/critical result or any Socket alert.
   - Inspect every Snyk medium/high/critical detail page. Continue only when the
     finding is inherent to the requested capability, the source and trust
     boundary are understood, and the risk is proportionate to the request.
   - Treat a missing table, missing provider column, or `--` result as
     unverified and stop unless the user explicitly accepts proceeding without
     that evidence.
   - Enter the literal `INSTALL` only after the gate passes. Any other response
     cancels without modifying the real global destinations.

4. Let the script perform the global install with the already-reviewed CLI
   version, then inspect its `skills list --global --json` output. Confirm the
   expected names are present for the selected agents and report missing entries
   instead of claiming a complete install.

## Selected Skills

Pass one `--skill` per requested name. The same disposable preflight, audit gate,
and exact-version reuse apply:

```bash
bash scripts/install_latest_pack.sh \
  --agent <target-agent-id> \
  --skill <skill-name> \
  --skill <another-skill-name>
```

If no `--skill` is supplied, the script installs the complete published pack.
If a requested skill is absent from `main`, the preflight fails; do not fall
back to a local path, feature branch, or commit.

## Ongoing Updates

To refresh only this pack or pick up newly published skills, repeat the audited
installer path above. This keeps the latest-at-start CLI version and audit
evidence coupled to the operation.

If the user explicitly wants every tracked global skill updated, including
skills installed from other sources, run the current npm `latest` CLI:

```bash
npx --yes skills@latest update --global --yes
```

That broad update path does not provide the same disposable partner-audit gate.
Use it only after stating the limitation and receiving explicit acceptance. For
named skills, put their names before `--global`. Updates run on demand, not in
the background.

## Gotchas

- `latest` means the npm `latest` dist-tag at operation start. The wrapper
  snapshots that version so a release cannot change between preflight and real
  installation.
- Running `skills@latest` still trusts the npm publisher and executes remote CLI
  code. A disposable workspace and npm cache contain expected writes but are not
  an OS sandbox or a substitute for package provenance.
- The preflight intentionally uses `--yes` only inside its disposable project.
  The real install uses `--yes` only after the separate `INSTALL` gate passes.
- Stop if the resolved version is empty, malformed, or differs from the CLI's
  own `--version` output.
- Stop if the latest CLI changes its output so the wrapper can no longer verify
  the audit table. Do not silently fall back to an older version or skip review.
- Keep `#main` explicit and quote the complete source. Do not use `@main`; the
  CLI interprets `@` as a skill filter rather than a Git branch.
- Do not use `--all`: it expands to every supported agent. Use the wrapper's
  repeated `--agent` arguments and its default full-pack skill selection.
- Global installation does not authorize deletion of unrelated or stale skills.
  Remove those only when the user explicitly names them.

## Output

Report the resolved Skills CLI version, source, selected agents and skills,
audit evidence reviewed, confirmation or cancellation, and verification result.
Do not claim that unmerged work was installed. On cancellation, identify the
finding and whether it is an inherent capability risk or unexplained blocker.
