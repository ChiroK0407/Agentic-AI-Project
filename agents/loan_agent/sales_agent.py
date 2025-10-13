from utils.mock_api import get_offer_data

def handle_sales(phone, amount, tenure, loan_type):
    """Handles discussion of loan amount, tenure, and interest based on loan type."""
    offer = get_offer_data(phone)
    if not offer:
        return f"❌ No pre-approved offer found for {phone}."

    # Customize summary by loan type
    if loan_type.lower() == "personal":
        intro = "🧍 Personal Loan Offer"
        notes = "Ideal for short-term needs like travel, education, or emergencies."
    elif loan_type.lower() == "home":
        intro = "🏠 Home Loan Offer"
        notes = "Designed for property purchase, renovation, or construction."
    elif loan_type.lower() == "business":
        intro = "💼 Business Loan Offer"
        notes = "Supports working capital, expansion, or equipment purchase."
    else:
        intro = "💬 General Loan Offer"
        notes = "Please verify the loan type for accurate details."

    response = (
        f"\n\n{intro}\n"
        f"\nPre-approved limit: ₹{offer['pre_approved_limit']:,}\n"
        f"Interest rate: {offer['interest_rate']}%\n"
        f"Requested loan: ₹{amount:,} for {tenure} years\n"
        f"\n📌 Notes: {notes}"
    )
    return response
