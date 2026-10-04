# Threat model
This is a local, single-user portfolio demo, with synthetic data only. It has no authentication or authorization. Bind to localhost; do not expose it to the Internet or submit real customer records.

| Threat | Current control | Remaining limitation |
|---|---|---|
| Script injection in case content | Browser escapes user content before rendering | No CSP policy yet |
| SQL injection | Parameterized statements | Local database is unencrypted |
| Concurrent lifecycle updates | Transaction and transition validation | No multi-user identity or roles |
| False-negative triage | Mandatory human review; evidence display | Review is a workflow assertion, not authenticated approval |
| Prompt injection | No live LLM in this release | Future providers need isolated prompts and validated outputs |
| Data leakage | No outbound model calls | Add retention, redaction and access controls before real data |

Audit events are append-only through the application, but a database owner can modify them. Production work would require identity, role authorization, tamper-resistant audit storage, retention controls, rate limiting and deployment security review.
