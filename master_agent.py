import re
import requests
from datetime import datetime
from agents.loan_agent import sales_agent, verification_agent, underwriting_agent, sanction_agent
from agents.card_agent import handle_card_issue
from agents.complaint_agent import handle_complaint
from utils.report_generator import generate_service_pdf
from utils.mock_api import get_credit_score
from utils.account_check import has_account
from dotenv import load_dotenv
import os
load_dotenv()


# -----------------------------
# Intent Detection (Router)
# -----------------------------
def detect_intent(user_input: str) -> str:
    """Detects which service domain the user wants help with."""
    text = user_input.lower()

    if re.search(r"loan|eligibility|apply|borrow|emi|personal|home|business", text):
        return "loan"
    elif re.search(r"card|debit|credit|transaction|payment", text):
        return "card"
    elif re.search(r"complaint|issue|problem|support|help", text):
        return "complaint"
    else:
        return "general"

# -----------------------------
# Domain-Specific Controllers
# -----------------------------
def handle_loan_service(name, phone, amount, tenure, loan_type="Personal"):
    """Executes the loan application pipeline using specialized worker agents."""
    if not has_account(phone):
        reply = (
            f"\n\n👋 Hello {name}, we couldn't find an account linked to your phone number.\n"
            f"Please explore our loan offers in the sidebar and consider joining JS Financial Services!"
        )
        return reply, None

    step1 = sales_agent.handle_sales(phone, amount, tenure, loan_type=loan_type)
    step2 = verification_agent.handle_verification(phone)

    # Calculate EMI and call underwriting
    emi = (amount / (tenure * 12)) * 1.1
    kyc_passed = "verified" in step2.lower()
    step3 = underwriting_agent.handle_underwriting(phone, amount, emi, kyc_passed=kyc_passed)

    # Sanction letter if approved
    pdf = None
    if "approved" in step3.lower():
        score = get_credit_score(phone)
        pdf = sanction_agent.generate_loan_sanction_letter(name, amount, tenure, step3, score)

    summary = f"""🧾 {loan_type} Loan Application Summary
{step1}
{step2}
{step3}
"""
    return summary, pdf

def handle_card_service(name, phone, card_last4, issue):
    """Handles card-related service requests."""
    if not (name and phone and card_last4 and issue):
        return "Please fill in your Name, Phone, Card Last 4 Digits, and Issue to continue.", None

    summary, ticket_id = handle_card_issue(name, phone, card_last4, issue)
    pdf = generate_service_pdf(name, phone, "Card Issue", summary, ticket_id)
    return summary, pdf

def handle_complaint_service(name, phone, complaint_text):
    """Handles complaints."""
    if not (name and phone and complaint_text):
        return "Please fill in your Name, Phone, and Complaint below to continue.", None

    summary, ticket_id = handle_complaint(name, phone, complaint_text)
    pdf = generate_service_pdf(name, phone, "Complaint", summary, ticket_id)
    return summary, pdf

def handle_general():
    """Default response when intent is unclear."""
    return (
        "\n\n👋 Welcome to JS Financial Services!\n"
        "I'm your virtual sales assistant. I can help you with:\n\n"
        "1️⃣ Personal, Home, or Business Loans\n"
        "2️⃣ Card or Payment Issues\n"
        "3️⃣ Filing a Complaint\n"
    )


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_llama(user_input):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
    "model": "llama-3.1-8b-instant",  # ✅ updated model
    "messages": [
        {"role": "system", "content": "You are a helpful loan assistant for JS Financial Services. You answer questions about loan eligibility, interest rates, EMI, and approval criteria in a friendly and professional tone."},
        {"role": "user", "content": user_input}
    ],
    "temperature": 0.7
    }


    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        data = response.json()
        print("LLM raw response:", data)
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ LLM Error: {data['error'].get('message', 'Unknown error')}"
        else:
            return "⚠️ Unexpected response from the language model."

    except Exception as e:
        return f"❌ Exception while querying LLM: {str(e)}"
# -----------------------------
# Master Agent: Core Orchestrator
# -----------------------------
def master_sales_agent(user_input, name=None, phone=None, amount=None, tenure=None, loan_type="Personal", card_last4=None, issue=None, complaint_text=None):
    """
    Main orchestrator that detects user intent, delegates tasks,
    and returns appropriate responses or file links.
    """
    text = user_input.strip().lower()

    if "loan" in text:
        intent = "loan"
    elif "card" in text:
        intent = "card"
    elif "complaint" in text:
        intent = "complaint"
    else:
        intent = detect_intent(user_input)

    # Route request
    if intent == "loan":
        if not (name and phone and amount and tenure):
            # If it's a general loan query, use LLM
            if user_input and len(user_input.strip()) > 10:
                reply = query_llama(user_input)
                return reply, None
            else:
                return "Please provide your name, phone, amount, and tenure in the form given below to continue.", None
        reply, pdf = handle_loan_service(name, phone, amount, tenure, loan_type=loan_type)

    elif intent == "card":
        if not (name and phone and card_last4 and issue):
            return "Please provide all card details to continue.", None
        reply, pdf = handle_card_service(name, phone, card_last4, issue)

    elif intent == "complaint":
        if not (name and phone and complaint_text):
            return "Please provide your name, phone, and complaint to continue.", None
        reply, pdf = handle_complaint_service(name, phone, complaint_text)

    else:
        reply = handle_general()
        pdf = None

    return reply, pdf