"""Explainable baseline. Recommendations always require human review."""
from dataclasses import dataclass, asdict
import re

POLICY = {
 'Security': ('Security', ['stolen', 'breach', 'malware', 'credential', 'compromised', 'unauthorized']),
 'Privacy': ('Privacy', ['personal data', 'private', 'sensitive', 'disclosed', 'pii']),
 'AI Safety': ('Trust & Safety', ['self-harm', 'dangerous', 'weapon', 'harmful']),
 'Reliability': ('Engineering', ['outage', 'unavailable', 'timeout', 'crash', '500']),
 'Account': ('Support', ['login', 'locked', 'password', 'access']),
 'Billing': ('Billing', ['invoice', 'charged', 'refund', 'payment']),
}
@dataclass
class Recommendation:
 category: str
 severity: str
 team: str
 evidence: list[str]
 review_required: bool = True
 method: str = 'rules-v1'

def triage(text: str) -> dict:
 lowered = text.lower()
 matches = {category: [word for word in words if re.search(r'\b'+re.escape(word)+r'\b',lowered)] for category, (_, words) in POLICY.items()}
 category = max(matches, key=lambda c: len(matches[c]))
 if not matches[category]: category = 'Other'
 team = POLICY[category][0] if category in POLICY else 'Support'
 evidence = matches.get(category, [])
 severity = 'P2'
 if category in ('Security', 'Privacy', 'AI Safety'): severity = 'P1'
 if any(x in lowered for x in ['all customers', 'ongoing breach', 'immediate danger', 'widespread outage']):
  severity='P0'; evidence += ['critical-impact phrase']
 elif category in ('Billing','Account','Other'): severity='P3'
 return asdict(Recommendation(category,severity,team,evidence))
