from datetime import datetime
from utils.account_check import has_account

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
    return summary, ticket_id