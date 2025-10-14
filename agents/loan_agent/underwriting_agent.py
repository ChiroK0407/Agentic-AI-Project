from utils.mock_api import get_credit_score, get_offer_data

def handle_underwriting(phone, loan_amount, emi, kyc_passed=True):
    if not kyc_passed:
        return f"Loan rejected due to failed KYC verification for phone: {phone}"
    
    credit_score = get_credit_score(phone)
    offer = get_offer_data(phone)

    if credit_score is None or offer is None:
        return "❌ Missing credit or offer data for underwriting."

    pre_limit = offer["pre_approved_limit"]
    score = credit_score  # fixed here

    if score < 700:
        return f"Loan rejected: Credit score {score} is below 700."
    elif loan_amount <= pre_limit:
        return f"Congratulations! Your Loan has been approved. Credit Score: {score}"
    elif loan_amount <= 2 * pre_limit and emi <= 0.5 * (pre_limit / 12):
        return f"Loan approved after salary verification. Credit Score: {score}."
    else:
        return f"Loan rejected: Requested ₹{loan_amount:,} exceeds approval limit."