from datetime import datetime
from utils.account_check import has_account

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
    return summary, ticket_id