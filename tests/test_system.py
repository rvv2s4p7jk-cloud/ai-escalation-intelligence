import pytest
from fastapi.testclient import TestClient
from backend.triage import triage
from backend.store import Store
from backend import app as module
@pytest.fixture
def client(tmp_path,monkeypatch):
 monkeypatch.setattr(module,'store',Store(str(tmp_path/'cases.db')))
 return TestClient(module.app)
def test_critical_impact():
 r=triage('Widespread outage affects all customers')
 assert r['severity']=='P0' and r['review_required']
def test_unknown_requires_review():
 assert triage('Please help with our question')['category']=='Other'
def test_lifecycle_and_audit(client):
 r=client.post('/api/cases',json={'title':'Token theft','description':'Stolen credentials caused an ongoing breach.'})
 assert r.status_code==201
 case=r.json();id=case['id']
 assert client.patch(f'/api/cases/{id}/status',json={'status':'Resolved','note':'Skip review'}).status_code==409
 r=client.patch(f'/api/cases/{id}/status',json={'status':'Triage','note':'Reviewer acknowledged security impact'})
 assert r.status_code==200 and len(r.json()['events'])==2
 assert client.get('/api/cases').json()[0]['status']=='Triage'
def test_input_and_missing_cases(client):
 assert client.post('/api/cases',json={'title':'x','description':'x'}).status_code==422
 assert client.get('/api/cases/missing').status_code==404
 assert client.patch('/api/cases/missing/status',json={'status':'Triage','note':'Reviewed'}).status_code==404
def test_persistence(tmp_path):
 path=str(tmp_path/'db');case=Store(path).create('API incident','API outage on one account')
 assert Store(path).get(case['id'])['title']=='API incident'
def test_dashboard(client):
 assert client.get('/').status_code==200
 assert client.get('/api/health').json()['status']=='ok'

def test_dataset_family_holdout():
 import json
 from pathlib import Path
 rows=json.loads((Path(__file__).resolve().parents[1]/'datasets/synthetic_escalations.json').read_text())
 train={r['family'] for r in rows if r['split']=='train'}
 test={r['family'] for r in rows if r['split']=='test'}
 assert train and test and train.isdisjoint(test)
