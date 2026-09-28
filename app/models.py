from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Ticket(Base):
    __tablename__="tickets"
    id: Mapped[str]=mapped_column(String(32),primary_key=True)
    customer_id: Mapped[str]=mapped_column(String(32),index=True)
    subject: Mapped[str]=mapped_column(String(250))
    description: Mapped[str]=mapped_column(Text())
    channel: Mapped[str]=mapped_column(String(30),default="email")
    status: Mapped[str]=mapped_column(String(30),default="open")
    priority: Mapped[str]=mapped_column(String(20),default="medium")
    team: Mapped[str|None]=mapped_column(String(40),nullable=True)
    confidence: Mapped[float|None]=mapped_column(Float,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))

class TriageAudit(Base):
    __tablename__="triage_audits"
    id: Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    ticket_id: Mapped[str]=mapped_column(String(32),index=True)
    decision: Mapped[dict]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
