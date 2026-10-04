# Architecture and decisions
FastAPI serves a lightweight browser dashboard and a REST API. The rule policy produces a category, severity, team and evidence; SQLite stores the case and transactional lifecycle events. Evaluation runs separately using TF-IDF/logistic regression trained exclusively on training families.

The first release intentionally favors a one-command local demo over distributed infrastructure. SQLite and plain JavaScript avoid PostgreSQL and React setup while preserving separable API and UI layers. The classifier and hybrid are benchmark experiments; the interactive API uses the deterministic rule baseline. No live LLM is implemented or measured.

Lifecycle: New → Triage → Investigation → Mitigation → Customer communication → Resolved → Post-incident review. Every transition requires a review/handoff note; skipped states are rejected.

Next steps: reviewer overrides and identity; provider-neutral structured LLM adapter; independent human annotations; React/TypeScript interface; PostgreSQL migration; SLA policy and timestamp-derived operational metrics. No invented SLA or resolution metrics are shown.
