import json
import os

def has_account(phone):
    path = os.path.join("data", "customers.json")
    if not os.path.exists(path):
        return False

    with open(path, "r") as f:
        customers = json.load(f)
        return any(str(c.get("phone", "")).strip() == str(phone).strip() for c in customers)