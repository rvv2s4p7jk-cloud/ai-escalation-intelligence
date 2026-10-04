# Signal · Escalation Intelligence

A local portfolio application for customer incident triage, cross-functional routing, and auditable response workflows. It combines customer operations judgment with cybersecurity risk analysis and measurable model evaluation.

**Status: working v0.1 portfolio demo. Synthetic data only. Human review required.**

## What you can do

- Create and inspect customer escalations in a responsive operations dashboard.
- Get rule-based severity, category, destination team, and matching evidence.
- Filter the queue by severity and inspect the audit history.
- Advance cases through validated lifecycle stages with review/handoff notes.
- Reproduce a rules vs supervised classifier vs hybrid benchmark, including prediction errors and confusion matrices.

## Run locally

Python 3.11+ is required. Run these commands inside the extracted repository folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Open http://localhost:8000 and select **Load sample cases**. The interactive API documentation is at http://localhost:8000/docs. On Windows, activate with `.venv\Scripts\activate`.

Alternatively, with Docker installed:

```bash
docker compose up --build
```

The SQLite database persists locally or in the Docker volume. No model key is needed. Do not expose this unauthenticated demo publicly or enter real customer information.

## Reproduce validation

```bash
python -m pytest -q
python -m evaluation.benchmark
```

Seven tests cover input validation, critical-impact triage, missing cases, persistence, audit events, rejected lifecycle jumps, static dashboard serving and scenario-family separation. JavaScript syntax was checked with Node. A full browser visual check and Docker build were not completed in the creation environment.

## Measured benchmark

112 synthetic cases; 56 training and 56 test cases; scenario families are disjoint. Four context variants per family are correlated. These results are diagnostic, not real-world performance estimates.

| Method | Category accuracy | Severity macro-F1 | Critical recall | Critical precision |
|---|---:|---:|---:|---:|
| rules | 14.3% | 0.150 | 0.0% | 0.0% |
| classifier | 28.6% | 0.016 | 95.8% | 46.9% |
| hybrid | 28.6% | 0.016 | 95.8% | 46.9% |

The rules miss critical paraphrases. The classifier's high critical recall accompanies low precision and extensive over-escalation; it is not evidence of a reliable production system. The test set has no P0 examples, limiting catastrophic-event conclusions. The hybrid does not improve this particular holdout because its safety overrides rarely trigger. See [evaluation protocol](docs/evaluation.md) and [complete predictions and errors](evaluation/results.json).

The UI uses rules only. The supervised classifier and hybrid are benchmark experiments. No live LLM performance is claimed. This initial release deliberately exposes baseline failure modes so later improvements can be measured against a committed baseline.

## Architecture

| Component | Implementation |
|---|---|
| API | FastAPI with validated request models |
| Dashboard | HTML/CSS/JavaScript, same-origin API |
| Triage | Evidence-producing keyword policy |
| Persistence | SQLite, parameterized SQL, transactional lifecycle updates |
| Evaluation | TF-IDF + logistic regression, family-based holdout |
| Automation | GitHub Actions: tests and benchmark |
| Packaging | Dockerfile and Compose configuration |

See [architecture decisions](docs/architecture.md) and [threat model](docs/threat-model.md).

## Dislaimer:

I built an incident triage application that turns customer reports into reviewable severity and routing recommendations. I also evaluated failure modes on held-out scenario families. The baseline missed paraphrases and the learned model over-escalated, which gave me a concrete roadmap for data quality, safety guardrails, and human oversight.

This is an independent project. It contains no sensitive data from any company, internal procedures, proprietary code or confidential incidents, and implies no company affiliation.

## Next milestones

1. Expand and freeze an independently labeled benchmark with P0 cases, negation and adversarial reports.
2. Add structured, provider-neutral LLM analysis and evaluate it against the committed baselines.
3. Implement authenticated reviewer overrides, secondary routing, escalation ownership and SLA policy.
4. Add PostgreSQL and React/TypeScript as deployment requirements grow.

MIT licensed. Current tested package versions are recorded in `requirements-tested.txt`; the main requirements file provides compatible version ranges.
