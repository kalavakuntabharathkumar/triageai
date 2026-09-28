from dataclasses import dataclass
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp=FastMCP("support-triage")

@dataclass
class LocalServices:
    tickets: dict[str,dict]
    customers: dict[str,dict]
    articles: list[dict]
    history: dict[str,list[dict]]
    audit: list[dict]

services=LocalServices(
    tickets={},
    customers={
        "CUST-1001":{"id":"CUST-1001","name":"Acme Retail","tier":"enterprise"},
        "CUST-1002":{"id":"CUST-1002","name":"Northwind Labs","tier":"standard"},
    },
    articles=[
        {"id":"KB-1","title":"Password reset","body":"Verify email delivery, spam folder and identity before reset escalation.","tags":["password","login"]},
        {"id":"KB-2","title":"Payment declined","body":"Check gateway response and billing status; billing team owns payment issues.","tags":["payment","billing"]},
        {"id":"KB-3","title":"API timeout","body":"Check status page, rate limits, recent deployments and API gateway logs.","tags":["api","timeout"]},
    ],
    history={},audit=[]
)

@mcp.tool()
def get_ticket(ticket_id: str)->dict[str,Any]:
    """Fetch the current ticket record."""
    return services.tickets.get(ticket_id,{"error":"ticket_not_found"})

@mcp.tool()
def search_knowledge_base(query: str)->list[dict[str,Any]]:
    """Search support knowledge articles by token overlap."""
    q=set(query.lower().split()); scored=[]
    for article in services.articles:
        hay=" ".join([article["title"],article["body"],*article["tags"]]).lower()
        score=sum(token in hay for token in q)
        if score: scored.append((score,article))
    return [a for _,a in sorted(scored,key=lambda x:x[0],reverse=True)[:3]]

@mcp.tool()
def get_customer(customer_id: str)->dict[str,Any]:
    """Fetch CRM customer profile."""
    return services.customers.get(customer_id,{"error":"customer_not_found"})

@mcp.tool()
def get_customer_history(customer_id: str)->list[dict[str,Any]]:
    """Fetch recent customer ticket history."""
    return services.history.get(customer_id,[])

@mcp.tool()
def update_ticket(ticket_id: str, fields: dict[str,Any])->dict[str,Any]:
    """Update ticket fields in the ticketing system."""
    if ticket_id not in services.tickets: return {"error":"ticket_not_found"}
    services.tickets[ticket_id].update(fields)
    return services.tickets[ticket_id]

@mcp.tool()
def assign_ticket(ticket_id: str, team: str)->dict[str,Any]:
    """Assign a ticket to a support team."""
    return update_ticket(ticket_id,{"team":team})

@mcp.tool()
def record_triage_decision(ticket_id: str, decision: dict[str,Any])->dict[str,Any]:
    """Persist an audit event for a triage decision."""
    event={"ticket_id":ticket_id,"decision":decision}; services.audit.append(event); return event
