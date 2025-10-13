import json
import os

DATA_PATH = "data"

def _load_json(filename):
    path = os.path.join(DATA_PATH, filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def get_customer_data(phone):
    customers = _load_json("customers.json")
    for customer in customers:
        if customer.get("phone") == phone:
            return customer
    return None  # if not found

def get_credit_score(phone):
    scores = _load_json("credit_score.json")
    return scores.get(phone)

def get_offer_data(phone):
    offers = _load_json("offers.json")
    return offers.get(phone)

def verify_customer(phone):
    customers = _load_json("customers.json")
    return phone in customers
