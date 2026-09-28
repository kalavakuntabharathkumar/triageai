from uuid import uuid4
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from .db import Base,engine,get_db
from .models import Ticket,TriageAudit
from .schemas import TicketCreate,TicketOut,TriageOut
from .mcp_tools import services
from .triage import triage_ticket

Base.metadata.create_all(bind=engine)
app=FastAPI(title="MCP Support Ticket Triage Agent",version="1.0.0")

@app.get("/health")
def health(): return {"status":"ok","service":"support-triage"}

@app.post("/tickets",response_model=TicketOut)
def create_ticket(payload:TicketCreate,db:Session=Depends(get_db)):
    ticket_id="TKT-"+uuid4().hex[:8].upper()
    ticket=Ticket(id=ticket_id,**payload.model_dump()); db.add(ticket); db.commit(); db.refresh(ticket)
    services.tickets[ticket_id]=payload.model_dump()|{"id":ticket_id,"status":"open","priority":"medium","team":None,"confidence":None}
    return ticket

@app.get("/tickets",response_model=list[TicketOut])
def list_tickets(db:Session=Depends(get_db)):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()

@app.get("/tickets/{ticket_id}",response_model=TicketOut)
def get_ticket(ticket_id:str,db:Session=Depends(get_db)):
    ticket=db.get(Ticket,ticket_id)
    if not ticket: raise HTTPException(404,"Ticket not found")
    return ticket

@app.post("/tickets/{ticket_id}/triage",response_model=TriageOut)
def triage(ticket_id:str,db:Session=Depends(get_db)):
    ticket=db.get(Ticket,ticket_id)
    if not ticket: raise HTTPException(404,"Ticket not found")
    services.tickets[ticket_id]={"id":ticket.id,"customer_id":ticket.customer_id,"subject":ticket.subject,"description":ticket.description,"channel":ticket.channel,"status":ticket.status,"priority":ticket.priority,"team":ticket.team,"confidence":ticket.confidence}
    result=triage_ticket(ticket_id)
    for key in ("status","priority","team","confidence"): setattr(ticket,key,services.tickets[ticket_id][key])
    db.add(TriageAudit(ticket_id=ticket_id,decision=result)); db.commit()
    return result

@app.get("/audits/{ticket_id}")
def audits(ticket_id:str,db:Session=Depends(get_db)):
    return db.query(TriageAudit).filter(TriageAudit.ticket_id==ticket_id).all()
