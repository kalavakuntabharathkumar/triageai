from app.triage import classify

def test_auth():
    c,t,conf,reasons=classify("Password reset email never arrives")
    assert c=="authentication" and t=="Identity & Access" and conf>=0.72 and reasons

def test_billing():
    c,t,*_=classify("Payment was declined"); assert c=="billing" and t=="Billing"

def test_general():
    c,t,conf,_=classify("I have a question"); assert c=="general" and t=="General Support" and conf==0.55
