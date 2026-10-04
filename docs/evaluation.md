# Evaluation protocol
112 synthetic cases represent 28 hand-authored scenario families with four context variants each. Training and testing use disjoint families (56 cases each). Labels are authored for portfolio demonstration; they have not been independently adjudicated. Context variants are correlated and do not constitute 112 independent observations.

Compare keyword rules, a supervised TF-IDF/logistic regression baseline, and a hybrid that preserves rule-generated P0/P1 recommendations. This is **not** an LLM comparison. The application runs rules; learned models are evaluation-only.

Category accuracy, severity macro-F1, routing accuracy and critical-event recall are computed from predictions. Routing is derived from category, so it is not an independent outcome. Confusion matrices use the fixed P0/P1/P2/P3 order. The test set contains no P0 cases, which limits conclusions about catastrophic-event detection; missing classes receive zero F1 in the fixed-label macro average. Inspect results.json for all errors.

Reproduce from the repository root: `python -m evaluation.benchmark`. Current policy and data were developed together, so this is a diagnostic benchmark rather than an unbiased estimate of real-world performance. A larger frozen test set, negation/adversarial examples, blinded labeling and uncertainty intervals are needed before comparing providers or claiming practical reliability.
