from app.db import Base,engine,SessionLocal
from app.models import Ticket
from app.mcp_tools import services
from app.triage import triage_ticket
Base.metadata.create_all(bind=engine); db=SessionLocal()
tid="TKT-DEMO01"; t=Ticket(id=tid,customer_id="CUST-1001",subject="Password reset broken",description="Urgent: password reset email is missing.",channel="email")
db.merge(t); db.commit()
services.tickets[tid]={"id":tid,"customer_id":"CUST-1001","subject":t.subject,"description":t.description,"channel":"email","status":"open","priority":"medium","team":None,"confidence":None}
print(triage_ticket(tid))
