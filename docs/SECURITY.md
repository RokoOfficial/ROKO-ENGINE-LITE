# Security considerations

ROKO ENGINE LITE is an automation runtime. It can execute registered tools from HTTP requests and from stored or submitted scripts. The code contains useful local safeguards, but it should be treated as a **trusted-network service by default** until the deployment adds the controls required for its audience and tool set.

## Controls present in the runtime

| Area | Current behavior | Scope |
|---|---|---|
| Expression evaluation | Uses a restricted Python AST allowlist and excludes function-call nodes | Limits expression syntax inside scripts |
| Tool invocation | Routes callable behavior through the `CALL` instruction and tool registry | Centralizes tool dispatch |
| Parser limits | Caps source lines, block depth, loop iterations, aggregate loop steps, and execution time | Reduces accidental runaway scripts |
| File names | Uses `secure_filename` and enforces the `.roko` extension | Restricts file API access to managed names |
| Upload payload | Sets Quart's maximum request content length to 2 MiB | Bounds individual HTTP request size |
| File locations | Separates repository examples from user uploads | Prevents API overwrites of shipped examples |
| Error details | Returns generic internal errors when debug mode is disabled | Avoids exposing stack details to ordinary callers |

These controls do not make every tool safe for every caller. The available registry includes network (`http.*`) and environment (`system.env`) capabilities. The risk profile changes as tools are added or as scripts become accessible to different users.

## Deployment requirements

| Risk area | Minimum production measure |
|---|---|
| Anonymous script or tool execution | Require authentication and authorization before protected routes |
| Cross-origin access | Replace the current wildcard CORS configuration with specific trusted origins |
| Secret management | Set `ROKO_SECRET_KEY` from a managed secret; do not rely on the development fallback |
| Transport security | Serve over HTTPS through a reverse proxy or load balancer |
| Outbound requests | Apply egress filtering, DNS protections, and target allowlists for `http.*` tools |
| Sensitive environment values | Filter or remove `system.env` for callers that should not inspect process configuration |
| Resource pressure | Add process-level CPU/memory limits, rate limiting, and concurrency controls |
| File retention | Use a durable, access-controlled storage strategy if uploaded scripts must persist |
| Logging | Avoid recording secrets from script inputs, headers, or tool parameters |

## Public exposure checklist

Before publishing the service behind a public hostname, confirm the following statements are true.

| Check | Expected state |
|---|---|
| Caller identity is authenticated | Yes |
| Caller permissions are evaluated for tool, script, and file operations | Yes |
| CORS origins are constrained to intended clients | Yes |
| `ROKO_SECRET_KEY` has a unique, non-default value | Yes |
| HTTPS and proxy timeouts are configured | Yes |
| HTTP tools cannot reach prohibited internal or metadata targets | Yes |
| Environment-sensitive tools are removed or permission-gated | Yes |
| Uploaded scripts and log files have an explicit retention policy | Yes |
| Observability avoids credentials and personal data | Yes |
| The release was checked with the validation procedure | Yes |

## Multi-tenant guidance

Do not treat the interpreter's expression restrictions as a sandbox for mutually untrusted users. The interpreter constrains the language grammar, but a registered tool determines what an execution can do. A multi-tenant design should isolate tenants at the process or workload boundary, use a narrowly curated registry per role, enforce quota and audit controls externally, and prevent one tenant's script or upload from being visible to another.

## Reporting and remediation

If a security concern is discovered, avoid publishing exploit details in an issue that could expose active deployments. First remove public exposure or restrict access, preserve relevant logs without secrets, rotate affected credentials, and patch or disable the implicated tool. Then add a regression test and document any change in public behavior in the changelog.
