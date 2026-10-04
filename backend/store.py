"""SQLite persistence with explicit lifecycle transitions and audit events."""
import sqlite3, json, os
from datetime import datetime, timezone
from uuid import uuid4
from backend.triage import triage
TRANSITIONS={'New':['Triage'],'Triage':['Investigation'],'Investigation':['Mitigation'],'Mitigation':['Customer communication'],'Customer communication':['Resolved'],'Resolved':['Post-incident review'],'Post-incident review':[]}
class Store:
 def __init__(self,path=None):
  self.path=path or os.getenv('DATABASE_PATH','cases.db')
  with self.connect() as db:
   db.executescript('CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,title TEXT,description TEXT,status TEXT,recommendation TEXT,created_at TEXT); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,case_id TEXT,at TEXT,action TEXT,note TEXT);')
 def connect(self):
  db=sqlite3.connect(self.path); db.row_factory=sqlite3.Row; return db
 def create(self,title,description):
  ident=str(uuid4()); now=datetime.now(timezone.utc).isoformat()
  with self.connect() as db:
   db.execute('INSERT INTO cases VALUES(?,?,?,?,?,?)',(ident,title,description,'New',json.dumps(triage(description)),now))
   db.execute('INSERT INTO events(case_id,at,action,note) VALUES(?,?,?,?)',(ident,now,'created','Synthetic/demo case'))
  return self.get(ident)
 def get(self,ident):
  with self.connect() as db:
   row=db.execute('SELECT * FROM cases WHERE id=?',(ident,)).fetchone()
   if not row: raise KeyError(ident)
   result=dict(row);result['recommendation']=json.loads(result['recommendation'])
   result['events']=[dict(e) for e in db.execute('SELECT at,action,note FROM events WHERE case_id=? ORDER BY id',(ident,))]
   return result
 def list(self):
  with self.connect() as db: ids=[r[0] for r in db.execute('SELECT id FROM cases ORDER BY created_at DESC')]
  return [self.get(i) for i in ids]
 def transition(self,ident,status,note):
  with self.connect() as db:
   db.execute('BEGIN IMMEDIATE')
   row=db.execute('SELECT status FROM cases WHERE id=?',(ident,)).fetchone()
   if not row: raise KeyError(ident)
   if status not in TRANSITIONS[row['status']]: raise ValueError('Invalid lifecycle transition')
   db.execute('UPDATE cases SET status=? WHERE id=?',(status,ident))
   db.execute('INSERT INTO events(case_id,at,action,note) VALUES(?,?,?,?)',(ident,datetime.now(timezone.utc).isoformat(),status,note))
  return self.get(ident)
