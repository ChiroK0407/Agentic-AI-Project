import json
import os

def handle_verification(phone):
    phone = str(phone).strip()

    # Load customer data
    data_path = os.path.join("data", "customers.json")
    if not os.path.exists(data_path):
        return f"⚠️ Customer database not found at {data_path}."

    with open(data_path, "r") as f:
        customers = json.load(f)

    # Search for matching phone number
    for customer in customers:
        if str(customer.get("phone", "")).strip() == phone:
            name = customer.get("name", "Unknown")
            address = customer.get("address", "Unknown")
            aadhaar = customer.get("aadhaar_verified", False)
            pan = customer.get("pan_verified", False)

            if aadhaar and pan:
                return f"\n\n✅ Full KYC verified for {name} from {address}."
            elif aadhaar or pan:
                return f"\n\n⚠️ Partial KYC verified for {name} from {address}. Please complete missing document verification."
            else:
                return f"\n\n❌ KYC failed for {name} from {address}. Neither Aadhaar nor PAN verified."

    return f"\n\n⚠️ Verification failed for phone: {phone}. No matching customer found."