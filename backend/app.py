from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from backend.store import Store
from backend.triage import triage
app=FastAPI(title='Escalation Intelligence',version='0.1.0')
store=Store()
class CaseInput(BaseModel):
 title: str=Field(min_length=3,max_length=150)
 description: str=Field(min_length=10,max_length=5000)
class Transition(BaseModel):
 status: str
 note: str=Field(min_length=5,max_length=1000)
@app.get('/api/health')
def health(): return {'status':'ok','mode':'local demo'}
@app.get('/api/cases')
def cases(): return store.list()
@app.post('/api/cases',status_code=201)
def create(case:CaseInput): return store.create(case.title,case.description)
@app.post('/api/triage')
def analyze(case:CaseInput): return triage(case.description)
@app.get('/api/cases/{ident}')
def get_case(ident:str):
 try: return store.get(ident)
 except KeyError: raise HTTPException(404,'Case not found')
@app.patch('/api/cases/{ident}/status')
def update(ident:str,change:Transition):
 try: return store.transition(ident,change.status,change.note)
 except KeyError: raise HTTPException(404,'Case not found')
 except ValueError as e: raise HTTPException(409,str(e))
app.mount('/',StaticFiles(directory=Path(__file__).resolve().parents[1]/'frontend',html=True),name='dashboard')
