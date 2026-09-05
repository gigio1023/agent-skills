import { afterAll, expect, test } from "bun:test";
import { join } from "node:path";

const secret = "fixture-secret-never-print";
const apiKey = "fixture-client-never-print";
const token = "fixture-token-never-print";
const account = "fixture-account-never-print";
const order = "fixture-order-never-print";
const payload = [secret, apiKey, token, account, order].join(" ");
let redirectedRequests = 0;
const sink = Bun.serve({
  hostname: "127.0.0.1",
  port: 0,
  fetch() {
    redirectedRequests += 1;
    return Response.json({});
  },
});
afterAll(() => sink.stop(true));

async function runScenario(stage: "token" | "account", response: () => Response) {
  let tokenRequests = 0;
  let accountRequests = 0;
  const server = Bun.serve({
    hostname: "127.0.0.1",
    port: 0,
    fetch(request) {
      const path = new URL(request.url).pathname;
      if (path === "/openapi-docs/latest/openapi.json") return Response.json({ paths: {} });
      if (path === "/oauth2/token") {
        tokenRequests += 1;
        if (stage === "token") return response();
        return Response.json({ access_token: token, token_type: "Bearer", expires_in: 3600 });
      }
      if (path === "/api/v1/accounts") {
        accountRequests += 1;
        return response();
      }
      return new Response(null, { status: 404 });
    },
  });
  try {
    const child = Bun.spawn([
      process.execPath, "--no-env-file", "--no-install",
      join(import.meta.dir, "fetch_portfolio_snapshot.ts"),
      "--base-url", server.url.origin, "--allow-custom-base-url", "--request-delay-ms", "0",
    ], {
      // Never inherit real credentials or user configuration in this test.
      env: { TOSS_INVEST_API_KEY: apiKey, TOSS_INVEST_SECRET_KEY: secret },
      stdout: "pipe", stderr: "pipe",
    });
    const [stdout, stderr, exitCode] = await Promise.all([
      new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited,
    ]);
    expect(exitCode).toBe(1);
    expect(tokenRequests).toBe(1);
    expect(accountRequests).toBe(stage === "account" ? 1 : 0);
    for (const sensitive of [secret, apiKey, token, account, order]) {
      expect(stdout + stderr).not.toContain(sensitive);
    }
    return JSON.parse(stderr).error as string;
  } finally {
    server.stop(true);
  }
}

for (const stage of ["token", "account"] as const) {
  for (const status of [307, 308]) {
    test(`${stage} request rejects HTTP ${status} without contacting another origin`, async () => {
      const before = redirectedRequests;
      const error = await runScenario(stage, () => new Response(null, {
        status, headers: { Location: sink.url.href },
      }));
      expect(error).toBe("API request failed; redirects are disabled");
      expect(redirectedRequests).toBe(before);
    });
  }
  test(`${stage} errors expose only the HTTP status`, async () => {
    const error = await runScenario(stage, () => Response.json({
      error: { code: payload, message: payload, requestId: payload },
    }, { status: 400, headers: { "X-Request-Id": payload } }));
    expect(error).toBe("API request failed: HTTP 400");
  });
  test(`${stage} malformed JSON never exposes parser excerpts`, async () => {
    const error = await runScenario(stage, () => new Response(`invalid JSON ${payload}`));
    expect(error).toBe("API response could not be read as JSON");
  });
}
