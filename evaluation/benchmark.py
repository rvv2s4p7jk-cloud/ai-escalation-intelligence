"""Scenario-family holdout evaluation; model learns only from training rows."""
import json
from pathlib import Path
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, confusion_matrix
from backend.triage import triage, POLICY
ROOT=Path(__file__).resolve().parents[1]
def run():
 rows=json.loads((ROOT/'datasets/synthetic_escalations.json').read_text())
 train=[r for r in rows if r['split']=='train']; test=[r for r in rows if r['split']=='test']
 assert set(r['family'] for r in train).isdisjoint(r['family'] for r in test)
 models={k:make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(max_iter=1000,random_state=42)) for k in ['category','severity']}
 for k,m in models.items(): m.fit([r['text'] for r in train],[r[k] for r in train])
 learned={k:m.predict([r['text'] for r in test]).tolist() for k,m in models.items()}
 rules=[triage(r['text']) for r in test]; report={'dataset_size':len(rows),'train_size':len(train),'test_size':len(test),'split':'held-out scenario families','results':{},'errors':[]}
 for mode in ['rules','classifier','hybrid']:
  categories=[]; severities=[]
  for i,r in enumerate(test):
   rule=rules[i]; cat=rule['category'] if mode=='rules' else learned['category'][i]; sev=rule['severity'] if mode=='rules' else learned['severity'][i]
   if mode=='hybrid' and rule['severity'] in ['P0','P1']: cat=rule['category'];sev=rule['severity']
   categories.append(cat);severities.append(sev)
   if cat!=r['category'] or sev!=r['severity']: report['errors'].append({'mode':mode,'id':r['id'],'text':r['text'],'expected_category':r['category'],'predicted_category':cat,'expected_severity':r['severity'],'predicted_severity':sev})
  true_cat=[r['category'] for r in test];true_sev=[r['severity'] for r in test]
  team=lambda cat: POLICY.get(cat,('Support',[]))[0]
  critical=[s in ['P0','P1'] for s in true_sev]
  report['results'][mode]={'category_accuracy':accuracy_score(true_cat,categories),'severity_macro_f1':f1_score(true_sev,severities,labels=['P0','P1','P2','P3'],average='macro',zero_division=0),'critical_recall':recall_score(critical,[s in ['P0','P1'] for s in severities],zero_division=0),'critical_precision':precision_score(critical,[s in ['P0','P1'] for s in severities],zero_division=0),'routing_accuracy':accuracy_score([team(c) for c in true_cat],[team(c) for c in categories]),'severity_confusion_labels':['P0','P1','P2','P3'],'severity_confusion_matrix':confusion_matrix(true_sev,severities,labels=['P0','P1','P2','P3']).tolist()}
 (ROOT/'evaluation/results.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k!='errors'},indent=2))
if __name__=='__main__': run()
