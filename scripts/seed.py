from app.db import Base,engine,SessionLocal
from app.models import Ticket
from app.mcp_tools import services
Base.metadata.create_all(bind=engine); db=SessionLocal()
samples=[("CUST-1001","Cannot reset my password","Reset email never arrives and I cannot sign in."),("CUST-1002","Payment failed","My card payment was declined during checkout."),("CUST-1001","API timeout","Our API integration returns timeout errors.")]
for i,(customer,subject,description) in enumerate(samples,1):
    tid=f"TKT-SEED{i:04d}"
    if not db.get(Ticket,tid): db.add(Ticket(id=tid,customer_id=customer,subject=subject,description=description,channel="email"))
    services.tickets[tid]={"id":tid,"customer_id":customer,"subject":subject,"description":description,"channel":"email","status":"open","priority":"medium","team":None,"confidence":None}
db.commit(); db.close(); print("Seeded 3 tickets.")
