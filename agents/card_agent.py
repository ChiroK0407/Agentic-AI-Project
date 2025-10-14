from datetime import datetime
import streamlit as st
from utils.account_check import has_account
from utils.report_generator import generate_service_pdf

def handle_card_issue(name, phone, card_last4, issue):
    if not has_account(phone):
        return (
            f"\n\n👋 Hello {name}, it looks like you don't have an account with us yet.\n"
            f"Please explore our offers in the sidebar to get started with JBank!"
        ), None

    ticket_id = f"CARD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    summary = (
        f"\n\n💳 Card Issue Registered\n"
        f"\n\nName: {name}\n"
        f"\n\nPhone: {phone}\n"
        f"\n\nCard Last 4 Digits: {card_last4}\n"
        f"\n\nIssue: {issue}\n"
        f"\n\nTicket ID: {ticket_id}"
    )
    pdf = generate_service_pdf(name, phone, "Card Issue", summary, ticket_id)
    return summary, pdf

def render_card_form(user_query):
    with st.form("card_form"):
        st.subheader("💳 Card Issue Form")
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        card_last4 = st.text_input("Last 4 Digits of Card")
        issue = st.text_area("Describe the Issue")
        submitted = st.form_submit_button("Submit Card Issue")

    if submitted:
        from master_agent import master_sales_agent
        reply, pdf = master_sales_agent(
            user_input=user_query,
            name=name,
            phone=phone,
            card_last4=card_last4,
            issue=issue
        )
        st.success(reply)
        if pdf:
            st.download_button("📄 Download Card Issue Report", data=pdf, file_name="card_issue.pdf")