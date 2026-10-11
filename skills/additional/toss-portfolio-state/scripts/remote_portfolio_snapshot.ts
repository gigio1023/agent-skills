#!/usr/bin/env bun

import { chmod, mkdir, readFile, rename, stat, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { hostname, homedir } from "node:os";
import { dirname, join, resolve } from "node:path";

type RemoteConfig = {
  version: 1;
  alias: string;
  host: string;
  user: string;
  keyPath: string;
};

type CommandResult = {
  exitCode: number;
  stdout: string;
  stderr: string;
};

const CONFIG_DIR = join(homedir(), ".config", "toss-portfolio-state");
const DEFAULT_CONFIG_PATH = join(CONFIG_DIR, "remote.json");
const SSH_DIR = join(homedir(), ".ssh");
const SSH_CONFIG_PATH = join(SSH_DIR, "config");
const SSH_CONFIG_DIR = join(SSH_DIR, "config.d");
const SSH_MANAGED_PATH = join(SSH_CONFIG_DIR, "toss-portfolio-state.conf");
const DEFAULT_ALIAS = "toss-home-api";
const DEFAULT_KEY_PATH = join(SSH_DIR, "id_ed25519_toss_portfolio_state");
const REMOTE_SCRIPT_DIR = ".local/share/toss-portfolio-state/scripts";
const REMOTE_FETCHER = `${REMOTE_SCRIPT_DIR}/fetch_portfolio_snapshot.ts`;
const REMOTE_TRANSPORT = `${REMOTE_SCRIPT_DIR}/remote_portfolio_snapshot.ts`;
const REMOTE_ENV_FILE = ".config/toss-invest/openapi.env";

const BOOLEAN_FETCH_FLAGS = new Set(["--help", "-h", "--self-test", "--print-api-coverage"]);
const VALUE_FETCH_FLAGS = new Set([
  "--account-alias",
  "--account-type",
  "--orders-days",
  "--recent-orders-limit",
  "--max-pages",
  "--request-delay-ms",
  "--symbols",
  "--market-context",
  "--market-indicators",
  "--market-symbol-limit",
  "--trade-count",
  "--candle-count",
  "--ranking-count",
]);
const FORBIDDEN_FETCH_FLAGS = new Set([
  "--env-file",
  "--base-url",
  "--allow-custom-base-url",
]);

function configPath(): string {
  const explicit = process.env.TOSS_PORTFOLIO_REMOTE_CONFIG;
  return explicit ? resolve(explicit) : DEFAULT_CONFIG_PATH;
}

function printUsage(): void {
  console.log(`Usage:
  bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts setup --host <tailscale-host> --user <ssh-user> [options]
  bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts fetch [snapshot-options]
  bun --no-env-file --no-install scripts/remote_portfolio_snapshot.ts --self-test

Setup options:
  --host <host>              Tailscale DNS name or IP of the home server.
  --user <user>              SSH user on the home server.
  --alias <alias>            Managed SSH alias. Default: ${DEFAULT_ALIAS}.
  --key-path <path>          Per-device Ed25519 key. Default: ${DEFAULT_KEY_PATH}.
  --bootstrap-host <host>    Existing passwordless SSH target used to authorize the new key.

The setup command writes personal connection state outside the skill directory.
The fetch command never falls back to a local Toss API request.`);
}

function assertSafeToken(label: string, value: string): void {
  if (!/^[A-Za-z0-9_.:-]+$/.test(value)) {
    throw new Error(`${label} contains unsupported characters`);
  }
}

function normalizeKeyPath(value: string): string {
  const expanded = value === "~" ? homedir() : value.startsWith("~/") ? join(homedir(), value.slice(2)) : value;
  const normalized = resolve(expanded);
  if (/\r|\n|"/.test(normalized)) {
    throw new Error("key path contains unsupported characters");
  }
  return normalized;
}

function validateConfig(value: unknown): RemoteConfig {
  if (!value || typeof value !== "object") {
    throw new Error("remote config must be an object");
  }
  const candidate = value as Partial<RemoteConfig>;
  if (candidate.version !== 1) {
    throw new Error("unsupported remote config version");
  }
  for (const field of ["alias", "host", "user", "keyPath"] as const) {
    if (typeof candidate[field] !== "string" || candidate[field]!.length === 0) {
      throw new Error(`remote config is missing ${field}`);
    }
  }
  assertSafeToken("SSH alias", candidate.alias!);
  assertSafeToken("SSH host", candidate.host!);
  assertSafeToken("SSH user", candidate.user!);
  return {
    version: 1,
    alias: candidate.alias!,
    host: candidate.host!,
    user: candidate.user!,
    keyPath: normalizeKeyPath(candidate.keyPath!),
  };
}

async function readConfigIfPresent(): Promise<RemoteConfig | null> {
  const path = configPath();
  if (!existsSync(path)) return null;
  const parsed = JSON.parse(await readFile(path, "utf8"));
  return validateConfig(parsed);
}

async function writeAtomic(path: string, content: string, mode: number): Promise<void> {
  await mkdir(dirname(path), { recursive: true, mode: 0o700 });
  const temporary = `${path}.tmp-${process.pid}`;
  await writeFile(temporary, content, { mode });
  await chmod(temporary, mode);
  await rename(temporary, path);
}

async function runCapture(command: string[]): Promise<CommandResult> {
  const child = Bun.spawn(command, { stdin: "ignore", stdout: "pipe", stderr: "pipe" });
  const [stdout, stderr, exitCode] = await Promise.all([
    new Response(child.stdout).text(),
    new Response(child.stderr).text(),
    child.exited,
  ]);
  return { exitCode, stdout, stderr };
}

async function runInteractive(command: string[]): Promise<number> {
  const child = Bun.spawn(command, { stdin: "inherit", stdout: "inherit", stderr: "inherit" });
  return await child.exited;
}

async function runWithInput(command: string[], input: string): Promise<number> {
  const child = Bun.spawn(command, { stdin: "pipe", stdout: "inherit", stderr: "inherit" });
  child.stdin.write(input);
  child.stdin.end();
  return await child.exited;
}

function parseSetupArgs(args: string[], existing: RemoteConfig | null): {
  config: RemoteConfig;
  bootstrapHost?: string;
} {
  const values: Record<string, string> = {};
  for (let index = 0; index < args.length; index += 2) {
    const flag = args[index];
    const value = args[index + 1];
    if (!["--host", "--user", "--alias", "--key-path", "--bootstrap-host"].includes(flag) || !value) {
      throw new Error(`invalid setup option near ${flag ?? "end of command"}`);
    }
    values[flag] = value;
  }

  const host = values["--host"] ?? existing?.host;
  const user = values["--user"] ?? existing?.user;
  const alias = values["--alias"] ?? existing?.alias ?? DEFAULT_ALIAS;
  const keyPath = values["--key-path"] ?? existing?.keyPath ?? DEFAULT_KEY_PATH;
  if (!host || !user) {
    throw new Error("setup requires --host and --user the first time");
  }
  assertSafeToken("SSH alias", alias);
  assertSafeToken("SSH host", host);
  assertSafeToken("SSH user", user);
  const bootstrapHost = values["--bootstrap-host"];
  if (bootstrapHost) assertSafeToken("bootstrap host", bootstrapHost);

  return {
    config: { version: 1, alias, host, user, keyPath: normalizeKeyPath(keyPath) },
    bootstrapHost,
  };
}

function renderManagedSshConfig(config: RemoteConfig): string {
  return `# Managed by toss-portfolio-state. Re-run setup to update.\nHost ${config.alias}\n    HostName ${config.host}\n    User ${config.user}\n    IdentityFile "${config.keyPath}"\n    IdentitiesOnly yes\n    ServerAliveInterval 30\n`;
}

async function ensureSshConfig(config: RemoteConfig): Promise<void> {
  await mkdir(SSH_DIR, { recursive: true, mode: 0o700 });
  await mkdir(SSH_CONFIG_DIR, { recursive: true, mode: 0o700 });
  await chmod(SSH_DIR, 0o700);
  await chmod(SSH_CONFIG_DIR, 0o700);

  const includeLine = "Include ~/.ssh/config.d/*";
  const current = existsSync(SSH_CONFIG_PATH) ? await readFile(SSH_CONFIG_PATH, "utf8") : "";
  const hasInclude = current.split(/\r?\n/).some((line) => line.trim() === includeLine);
  const next = hasInclude ? current : `${includeLine}\n\n${current}`;
  await writeAtomic(SSH_CONFIG_PATH, next.endsWith("\n") ? next : `${next}\n`, 0o600);
  await writeAtomic(SSH_MANAGED_PATH, renderManagedSshConfig(config), 0o600);
}

async function ensureKey(config: RemoteConfig): Promise<void> {
  const publicKeyPath = `${config.keyPath}.pub`;
  if (existsSync(config.keyPath) && existsSync(publicKeyPath)) return;
  if (existsSync(config.keyPath) || existsSync(publicKeyPath)) {
    throw new Error(`incomplete SSH key pair at ${config.keyPath}`);
  }
  await mkdir(dirname(config.keyPath), { recursive: true, mode: 0o700 });
  const exitCode = await runInteractive([
    "ssh-keygen",
    "-t",
    "ed25519",
    "-N",
    "",
    "-C",
    `toss-portfolio-state@${hostname()}`,
    "-f",
    config.keyPath,
  ]);
  if (exitCode !== 0) throw new Error("ssh-keygen failed");
  await chmod(config.keyPath, 0o600);
  await chmod(publicKeyPath, 0o644);
}

async function sshReady(alias: string): Promise<boolean> {
  const result = await runCapture([
    "ssh",
    "-T",
    "-o",
    "BatchMode=yes",
    "-o",
    "ConnectTimeout=10",
    alias,
    "true",
  ]);
  return result.exitCode === 0;
}

async function authorizeKey(config: RemoteConfig, bootstrapHost?: string): Promise<void> {
  if (await sshReady(config.alias)) return;
  const publicKey = await readFile(`${config.keyPath}.pub`, "utf8");
  if (!publicKey.startsWith("ssh-ed25519 ")) {
    throw new Error("unexpected SSH public-key format");
  }

  if (bootstrapHost) {
    const remoteCommand = 'set -eu; umask 077; mkdir -p "$HOME/.ssh"; touch "$HOME/.ssh/authorized_keys"; chmod 700 "$HOME/.ssh"; chmod 600 "$HOME/.ssh/authorized_keys"; IFS= read -r key; grep -qxF "$key" "$HOME/.ssh/authorized_keys" || printf "%s\\n" "$key" >> "$HOME/.ssh/authorized_keys"';
    const exitCode = await runWithInput(["ssh", "-T", bootstrapHost, remoteCommand], publicKey);
    if (exitCode !== 0) throw new Error("failed to authorize the new key through --bootstrap-host");
  } else {
    console.error("One-time SSH password authentication may be requested to authorize this device key.");
    const exitCode = await runInteractive([
      "ssh-copy-id",
      "-i",
      `${config.keyPath}.pub`,
      "-o",
      "StrictHostKeyChecking=accept-new",
      config.alias,
    ]);
    if (exitCode !== 0) throw new Error("ssh-copy-id failed");
  }

  if (!(await sshReady(config.alias))) {
    throw new Error("the managed SSH alias still cannot authenticate without a password");
  }
}

async function deployRemoteScripts(config: RemoteConfig): Promise<void> {
  const prepare = await runCapture([
    "ssh",
    "-T",
    config.alias,
    'set -eu; test -x "$HOME/.bun/bin/bun"; test -f "$HOME/.config/toss-invest/openapi.env"; mkdir -p "$HOME/.local/share/toss-portfolio-state/scripts"; chmod 700 "$HOME/.local/share/toss-portfolio-state" "$HOME/.local/share/toss-portfolio-state/scripts"',
  ]);
  if (prepare.exitCode !== 0) {
    throw new Error(`home server is missing Bun, its Toss env file, or the target directory: ${prepare.stderr.trim()}`);
  }

  const localDirectory = import.meta.dir;
  const files = ["fetch_portfolio_snapshot.ts", "remote_portfolio_snapshot.ts"];
  for (const file of files) {
    const source = join(localDirectory, file);
    const remoteTemporary = `${REMOTE_SCRIPT_DIR}/${file}.new-${process.pid}`;
    const copy = await runCapture(["scp", "-q", source, `${config.alias}:${remoteTemporary}`]);
    if (copy.exitCode !== 0) throw new Error(`failed to upload ${file}: ${copy.stderr.trim()}`);
  }

  const installCommand = `set -eu; install -m 600 "$HOME/${REMOTE_FETCHER}.new-${process.pid}" "$HOME/${REMOTE_FETCHER}"; install -m 600 "$HOME/${REMOTE_TRANSPORT}.new-${process.pid}" "$HOME/${REMOTE_TRANSPORT}"; rm -f "$HOME/${REMOTE_FETCHER}.new-${process.pid}" "$HOME/${REMOTE_TRANSPORT}.new-${process.pid}"; "$HOME/.bun/bin/bun" --no-env-file --no-install "$HOME/${REMOTE_TRANSPORT}" --self-test`;
  const installResult = await runCapture(["ssh", "-T", config.alias, installCommand]);
  if (installResult.exitCode !== 0) {
    throw new Error(`remote script install or self-test failed: ${installResult.stderr.trim()}`);
  }
}

function validateFetchArgs(args: string[]): void {
  for (let index = 0; index < args.length; index += 1) {
    const flag = args[index];
    if (FORBIDDEN_FETCH_FLAGS.has(flag)) {
      throw new Error(`${flag} is blocked on the home-server route`);
    }
    if (BOOLEAN_FETCH_FLAGS.has(flag)) continue;
    if (VALUE_FETCH_FLAGS.has(flag)) {
      if (index + 1 >= args.length || args[index + 1].startsWith("--")) {
        throw new Error(`${flag} requires a value`);
      }
      index += 1;
      continue;
    }
    throw new Error(`unsupported snapshot option: ${flag}`);
  }
}

function encodeArgs(args: string[]): string {
  validateFetchArgs(args);
  return Buffer.from(JSON.stringify(args), "utf8").toString("base64url");
}

function decodeArgs(payload: string): string[] {
  if (!payload || payload.length > 16_384 || !/^[A-Za-z0-9_-]+$/.test(payload)) {
    throw new Error("invalid encoded argument payload");
  }
  const parsed = JSON.parse(Buffer.from(payload, "base64url").toString("utf8"));
  if (!Array.isArray(parsed) || !parsed.every((value) => typeof value === "string" && !value.includes("\0"))) {
    throw new Error("decoded arguments must be strings");
  }
  validateFetchArgs(parsed);
  return parsed;
}

async function setup(args: string[]): Promise<void> {
  const existing = await readConfigIfPresent();
  const { config, bootstrapHost } = parseSetupArgs(args, existing);
  await ensureKey(config);
  await ensureSshConfig(config);

  const sshExpansion = await runCapture(["ssh", "-G", config.alias]);
  if (sshExpansion.exitCode !== 0) throw new Error("managed SSH config is invalid");
  await authorizeKey(config, bootstrapHost);
  await deployRemoteScripts(config);
  await writeAtomic(configPath(), `${JSON.stringify(config, null, 2)}\n`, 0o600);

  console.log(JSON.stringify({
    ok: true,
    action: "setup",
    alias: config.alias,
    host: config.host,
    config_path: configPath(),
    key_path: config.keyPath,
    remote_scripts_deployed: true,
  }, null, 2));
}

async function fetchViaRemote(args: string[]): Promise<void> {
  const config = await readConfigIfPresent();
  if (!config) {
    throw new Error(`remote setup is missing; run the setup command first (${configPath()})`);
  }
  const payload = encodeArgs(args);
  const remoteCommand = `"$HOME/.bun/bin/bun" --no-env-file --no-install "$HOME/${REMOTE_TRANSPORT}" remote-run ${payload}`;
  const exitCode = await runInteractive(["ssh", "-T", config.alias, remoteCommand]);
  if (exitCode !== 0) {
    throw new Error(`home-server snapshot failed with exit code ${exitCode}; no local fallback was attempted`);
  }
}

async function runRemote(payload: string): Promise<void> {
  const args = decodeArgs(payload);
  const envPath = join(homedir(), REMOTE_ENV_FILE);
  const fetcherPath = join(import.meta.dir, "fetch_portfolio_snapshot.ts");
  const envStat = await stat(envPath);
  if ((envStat.mode & 0o077) !== 0) {
    throw new Error("remote Toss env file permissions must not grant group or other access");
  }
  const exitCode = await runInteractive([
    process.execPath,
    "--no-env-file",
    "--no-install",
    fetcherPath,
    "--env-file",
    envPath,
    ...args,
  ]);
  process.exitCode = exitCode;
}

function selfTest(): void {
  const fixture = ["--market-context", "basic", "--orders-days", "30", "--symbols", "000660,NBIS"];
  const decoded = decodeArgs(encodeArgs(fixture));
  if (JSON.stringify(decoded) !== JSON.stringify(fixture)) throw new Error("argument round trip failed");
  for (const forbidden of FORBIDDEN_FETCH_FLAGS) {
    let rejected = false;
    try {
      validateFetchArgs(forbidden === "--allow-custom-base-url" ? [forbidden] : [forbidden, "value"]);
    } catch {
      rejected = true;
    }
    if (!rejected) throw new Error(`${forbidden} was not rejected`);
  }
  const sample = validateConfig({
    version: 1,
    alias: "toss-home-api",
    host: "server.example.ts.net",
    user: "investor",
    keyPath: "~/.ssh/id_ed25519_toss_portfolio_state",
  });
  if (!renderManagedSshConfig(sample).includes("IdentitiesOnly yes")) {
    throw new Error("managed SSH config is incomplete");
  }
  console.log(JSON.stringify({
    ok: true,
    test: "remote_portfolio_snapshot self-test",
    argument_round_trip: true,
    unsafe_override_gate: true,
    managed_ssh_config: true,
  }, null, 2));
}

async function main(): Promise<void> {
  const [command, ...args] = process.argv.slice(2);
  if (command === "--self-test") {
    selfTest();
    return;
  }
  if (command === "--help" || command === "-h" || !command) {
    printUsage();
    if (!command) process.exitCode = 2;
    return;
  }
  if (command === "setup") {
    await setup(args);
    return;
  }
  if (command === "fetch") {
    await fetchViaRemote(args);
    return;
  }
  if (command === "remote-run") {
    if (args.length !== 1) throw new Error("remote-run requires one encoded argument payload");
    await runRemote(args[0]);
    return;
  }
  throw new Error(`unknown command: ${command}`);
}

main().catch((error) => {
  console.error(`remote_portfolio_snapshot: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
