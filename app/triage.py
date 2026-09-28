import re
from .mcp_tools import services,get_customer,get_customer_history,search_knowledge_base,assign_ticket,update_ticket,record_triage_decision

CATEGORIES={
 "authentication":("Identity & Access",["password","login","reset","signin","sign in","2fa","otp"]),
 "billing":("Billing",["payment","invoice","refund","charge","billing","subscription"]),
 "technical":("Technical Support",["api","error","timeout","crash","bug","integration","500","failed"]),
}

def classify(text):
    t=text.lower()
    scores={k:sum(bool(re.search(r"\b"+re.escape(w)+r"\b",t)) for w in words) for k,(_,words) in CATEGORIES.items()}
    category,score=max(scores.items(),key=lambda x:x[1])
    if score==0: return "general","General Support",0.55,["No strong category keyword matched."]
    return category,CATEGORIES[category][0],min(0.97,0.72+score*0.08),[f"Matched {score} category signal(s) for {category}."]

def triage_ticket(ticket_id):
    ticket=services.tickets[ticket_id]
    customer=get_customer(ticket["customer_id"])
    history=get_customer_history(ticket["customer_id"])
    articles=search_knowledge_base(ticket["subject"]+" "+ticket["description"])
    category,team,confidence,rationale=classify(ticket["subject"]+" "+ticket["description"])
    priority="high" if customer.get("tier")=="enterprise" or "urgent" in ticket["description"].lower() else "medium"
    if len(history)>=3: rationale.append("Customer has multiple recent tickets; prioritize continuity.")
    if articles: rationale.append(f"Found {len(articles)} relevant knowledge article(s).")
    update_ticket(ticket_id,{"priority":priority,"status":"triaged","team":team,"confidence":confidence})
    assign_ticket(ticket_id,team)
    decision={"category":category,"team":team,"priority":priority,"confidence":confidence,"rationale":rationale}
    record_triage_decision(ticket_id,decision)
    return {"ticket_id":ticket_id,**decision,"tools_used":["get_ticket","get_customer","get_customer_history","search_knowledge_base","update_ticket","assign_ticket","record_triage_decision"]}
