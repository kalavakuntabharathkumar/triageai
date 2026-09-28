from app.mcp_tools import services,get_ticket,search_knowledge_base,get_customer,get_customer_history

def test_tools():
    services.tickets["T"]={"id":"T"}
    assert get_ticket("T")["id"]=="T"
    assert get_customer("CUST-1001")["tier"]=="enterprise"
    assert search_knowledge_base("password reset")
    assert get_customer_history("CUST-1001")==[]
