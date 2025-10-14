from datetime import datetime
import streamlit as st
from utils.account_check import has_account
from utils.report_generator import generate_service_pdf

def handle_complaint(name, phone, complaint_type, description):
    if not has_account(phone):
        return (
            f"\n\n👋 Hi {name}, we couldn't find an account linked to your phone number.\n"
            f"Feel free to check out our offers in the sidebar and join JBank today!"
        ), None

    ticket_id = f"COMP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    summary = (
        f"\n\n🛠️ Complaint Registered\n"
        f"\n\nName: {name}\n"
        f"\n\nPhone: {phone}\n"
        f"\n\nComplaint Type: {complaint_type}\n"
        f"\n\nDescription: {description}\n"
        f"\n\nTicket ID: {ticket_id}"
    )
    pdf = generate_service_pdf(name, phone, "Complaint", summary, ticket_id)
    return summary, pdf

def render_complaint_form(user_query):
    with st.form("complaint_form"):
        st.subheader("📝 Complaint Form")
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        complaint_type = st.selectbox("Complaint Type", ["Transaction", "Service", "App", "Other"])
        description = st.text_area("Describe Your Complaint")
        submitted = st.form_submit_button("Submit Complaint")

    if submitted:
        from master_agent import master_sales_agent
        reply, pdf = master_sales_agent(
            user_input=user_query,
            name=name,
            phone=phone,
            complaint_text=f"{complaint_type}: {description}"
        )
        st.success(reply)
        if pdf:
            st.download_button("📄 Download Complaint Report", data=pdf, file_name="complaint.pdf")