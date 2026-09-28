from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    subject: str=Field(min_length=3,max_length=250)
    description: str=Field(min_length=3)
    customer_id: str
    channel: str="email"

class TicketOut(TicketCreate):
    id: str
    status: str
    priority: str
    team: str|None=None
    confidence: float|None=None
    model_config={"from_attributes":True}

class TriageOut(BaseModel):
    ticket_id: str
    category: str
    team: str
    priority: str
    confidence: float
    rationale: list[str]
    tools_used: list[str]
