import streamlit as st
from master_agent import master_sales_agent
import os

# -----------------------------------------
# Page Setup
# -----------------------------------------
st.set_page_config(page_title="Agentic AI Sales Assistant", page_icon="🤖", layout="centered")

with st.sidebar:
    st.markdown("### 🏦 Welcome to JS Financial Services!")
    st.write("I'm your digital sales assistant. Explore our latest loan products or start your application.")
    
    if st.button("🎁 View Loan Offers"):
        st.session_state.show_offers = True

# -----------------------------------------
# Custom CSS for clean layout & chat bubbles
# -----------------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
.user-msg {
    background-color: #DCF8C6;
    padding: 10px 14px;
    border-radius: 15px;
    margin-bottom: 6px;
    margin-left: 30%;
    text-align: right;
    max-width: 70%;
}
.ai-msg {
    background-color: #F1F0F0;
    padding: 10px 14px;
    border-radius: 15px;
    margin-bottom: 6px;
    margin-right: 30%;
    text-align: left;
    max-width: 70%;
}
.stButton>button {
    background-color: #004AAD;
    color: white;
    border-radius: 8px;
    padding: 6px 20px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Page Title
# -----------------------------------------
st.title("🤖 Agentic AI Sales Assistant")
st.markdown("Welcome! I'm your virtual assistant from JS Financial Services. Type your query or choose a service: (loan, card, complaint)")

# -----------------------------------------
# Initialize session state
# -----------------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []
if "intent" not in st.session_state:
    st.session_state["intent"] = None
if "pdf" not in st.session_state:
    st.session_state["pdf"] = None
if "form_triggered" not in st.session_state:
    st.session_state["form_triggered"] = False
if "loan_type" not in st.session_state:
    st.session_state["loan_type"] = None

# -----------------------------------------
# Display chat messages
# -----------------------------------------
for sender, msg in st.session_state["history"]:
    bubble = "user-msg" if sender == "🧍 You" else "ai-msg"
    st.markdown(f"<div class='{bubble}'>{msg}</div>", unsafe_allow_html=True)

# -----------------------------------------
# Input section
# -----------------------------------------
user_input = st.text_input("💬 You:", placeholder="Type your query here...")

if st.button("Send"):
    reply, pdf = master_sales_agent(user_input, loan_type=st.session_state.get("loan_type"))
    st.session_state["history"].append(("🧍 You", user_input))
    st.session_state["history"].append(("🤖 AI", reply))
    st.session_state["pdf"] = pdf

    # Intent detection
    text = user_input.lower().strip()
    if "loan" in text:
        st.session_state["intent"] = "loan"
        st.session_state["form_triggered"] = False
        st.session_state["loan_type"] = None
    elif "card" in text:
        st.session_state["intent"] = "card"
    elif "complaint" in text:
        st.session_state["intent"] = "complaint"
    else:
        st.session_state["intent"] = None

    # Clear chatbox by rerunning without modifying session_state["user_input"]
    st.rerun()

# -----------------------------------------
# Dynamic Forms
# -----------------------------------------
if st.session_state["intent"] == "loan" and st.session_state["form_triggered"]:
    st.markdown("---")
    st.subheader("📋 Loan Application Form")
    name = st.text_input("Name:")
    phone = st.text_input("Phone:")
    amount = st.number_input("Loan Amount (₹):", min_value=10000, max_value=2000000, value=100000)
    tenure = st.number_input("Tenure (years):", min_value=1, max_value=10, value=2)

    if st.session_state["loan_type"]:
        loan_type = st.session_state["loan_type"]
    else:
        loan_type = st.selectbox("Select Loan Type:", ["Personal", "Home", "Business"])

    if st.button("Submit Loan Application"):
        st.session_state["form_triggered"] = True
        if not all([name.strip(), phone.strip()]):
            st.error("❌ Please fill in all fields.")
        else:
            reply, pdf = master_sales_agent("loan", name=name, phone=phone, amount=amount, tenure=tenure, loan_type=loan_type)
            st.session_state["history"].append(("🧍 You", f"{loan_type} Loan application for ₹{amount:,}"))
            st.session_state["history"].append(("🤖 AI", reply))
            st.session_state["pdf"] = pdf
            st.rerun()

elif st.session_state["intent"] == "card":
    st.markdown("---")
    st.subheader("💳 Card Assistance Form")
    name = st.text_input("Name:")
    phone = st.text_input("Phone:")
    card_last4 = st.text_input("Card Last 4 Digits:")
    issue = st.text_area("Describe the issue:")

    if st.button("Submit Card Issue"):
        if not all([name.strip(), phone.strip(), card_last4.strip(), issue.strip()]):
            st.error("❌ Please fill in all fields.")
        else:
            reply, pdf = master_sales_agent("card", name=name, phone=phone, card_last4=card_last4, issue=issue)
            st.session_state["history"].append(("🧍 You", f"Card Issue: {issue}"))
            st.session_state["history"].append(("🤖 AI", reply))
            st.session_state["pdf"] = pdf
            st.rerun()

elif st.session_state["intent"] == "complaint":
    st.markdown("---")
    st.subheader("📝 Complaint Form")
    name = st.text_input("Name:")
    phone = st.text_input("Phone:")
    complaint_text = st.text_area("Describe your complaint:")

    if st.button("Submit Complaint"):
        if not all([name.strip(), phone.strip(), complaint_text.strip()]):
            st.error("❌ Please fill in all fields.")
        else:
            reply, pdf = master_sales_agent("complaint", name=name, phone=phone, complaint_text=complaint_text)
            st.session_state["history"].append(("🧍 You", "Filed a complaint"))
            st.session_state["history"].append(("🤖 AI", reply))
            st.session_state["pdf"] = pdf
            st.rerun()

# -----------------------------------------
# Loan Offers Section
# -----------------------------------------
if st.session_state.get("show_offers"):
    st.markdown("### 💼 Current Loan Products")
    st.write("""
    - **Personal Loan**: Up to ₹5,00,000 @ 12.5%  
    - **Home Loan**: Up to ₹50,00,000 @ 9.2%  
    - **Business Loan**: Up to ₹25,00,000 @ 11.0%  
    - **Education Loan**: Up to ₹10,00,000 @ 10.8%  
    - **Vehicle Loan**: Up to ₹8,00,000 @ 11.3%
    """)

# -----------------------------------------
# PDF Download
# -----------------------------------------
if st.session_state.get("pdf"):
    pdf = st.session_state["pdf"]
    if os.path.exists(pdf):
        with open(pdf, "rb") as f:
            st.download_button("📄 Download Loan Sanction Letter", f, file_name=os.path.basename(pdf), mime="application/pdf")
    else:
        st.error("⚠️ PDF file not found.")