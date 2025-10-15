import streamlit as st
from master_agent import master_sales_agent, query_llama
from agents.card_agent import render_card_form
from agents.complaint_agent import render_complaint_form

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="JS Financial Assistant", page_icon="💼")
st.title("💬 JS Financial Services Assistant")

# -----------------------------
# Session Initialization
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant for JS Financial Services. "
                "You answer questions about loans, card issues, and complaints in a friendly and professional tone. "
                "When users ask about services, always guide them to type:\n"
                "1️⃣ for Personal Loan\n2️⃣ for Business Loan\n3️⃣ for Home Loan\n"
                "4️⃣ for Card Issue\n5️⃣ for Complaint"
            )
        }
    ]

if "triggered_loan_type" not in st.session_state:
    st.session_state.triggered_loan_type = None

if "intent" not in st.session_state:
    st.session_state.intent = None

# -----------------------------
# Sidebar Greeting
# -----------------------------
with st.sidebar:
    st.markdown("### 👋 Welcome!")
    st.markdown("We're here to help you with loans, card issues, and complaints — all in one place.")
    st.button("🎁 View Offers")

# -----------------------------
# Chat Input
# -----------------------------
user_query = st.text_input("💬 Type your message or press 1️⃣–5️⃣ to begin:")

if user_query:
    if user_query.strip() in ["1", "2", "3", "4", "5"]:
        # Skip LLM, just trigger form
        _, triggered_type = query_llama(user_query, st.session_state.chat_history)

        if triggered_type in ["Personal", "Business", "Home"]:
            st.session_state.triggered_loan_type = triggered_type
            st.markdown(f"✅ {triggered_type} Loan selected. Please fill out the form below.")

        elif triggered_type == "Card":
            st.session_state.intent = "card"
            st.markdown("✅ Card Issue selected. Please fill out the form below.")

        elif triggered_type == "Complaint":
            st.session_state.intent = "complaint"
            st.markdown("✅ Complaint selected. Please fill out the form below.")

    else:
        # Let LLM handle natural language
        reply, triggered_type = query_llama(user_query, st.session_state.chat_history)
        st.markdown(reply.replace("\t", "    "))

# -----------------------------
# Loan Form
# -----------------------------
if st.session_state.triggered_loan_type:
    with st.form("loan_form"):
        st.subheader(f"📋 {st.session_state.triggered_loan_type} Loan Application Form")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        amount = st.number_input("Loan Amount", min_value=1000)
        tenure = st.number_input("Tenure (in years)", min_value=1)
        submitted = st.form_submit_button("Submit Application")

    if submitted:
        reply, pdf = master_sales_agent(
            user_input=f"Apply for a {st.session_state.triggered_loan_type} loan",
            name=name,
            phone=phone,
            amount=amount,
            tenure=tenure,
            loan_type=st.session_state.triggered_loan_type
        )
        st.success(reply)
        if pdf:
            st.download_button("📄 Download Sanction Letter", data=pdf, file_name="sanction_letter.pdf")

# -----------------------------
# Card and Complaint Forms
# -----------------------------
if st.session_state.intent == "card":
    render_card_form(user_query)

if st.session_state.intent == "complaint":
    render_complaint_form(user_query)

# -----------------------------
# Footer Reset Button
# -----------------------------
st.divider()
if st.button("Reset Conversation"):
    try:
        keys_to_clear = list(st.session_state.keys())
        for key in keys_to_clear:
            del st.session_state[key]
        st.experimental_rerun()
    except Exception as e:
        st.warning(f"Unable to reset. Error: {e}")