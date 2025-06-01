from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Paystack Secret Key
PAYSTACK_SECRET = 'sk_live_a9dfd83efcc1addd939a8bbd985dde022a05a54c'  # Replace with your actual secret key

@app.route("/ussd", methods=["POST"])
def ussd():
    session_id = request.form.get("sessionId")
    service_code = request.form.get("serviceCode")
    phone_number = request.form.get("phoneNumber")
    text = request.form.get("text", "")

    inputs = text.split("*")
    user_response = ""

    if text == "":
        user_response = "CON Welcome to Flap Market\n1. Buy Bread\n2. Exit"
    elif text == "1":
        user_response = "CON Enter quantity of Bread:"
    elif inputs[0] == "1" and len(inputs) == 2:
        qty = int(inputs[1])
        total_price = qty * 5  # e.g., 5 GHS per bread
        user_response = f"CON Total: GHS {total_price}\n1. Confirm\n2. Cancel"
    elif inputs[0] == "1" and len(inputs) == 3:
        qty = int(inputs[1])
        total_price = qty * 5
        if inputs[2] == "1":
            # Trigger Paystack MoMo charge
            payment_response = initiate_paystack_charge(phone_number, total_price)
            if payment_response.get("status"):
                user_response = "END Order confirmed. MoMo Payment initiated."
            else:
                user_response = f"END Failed to initiate payment: {payment_response.get('message')}"
        else:
            user_response = "END Order cancelled."
    else:
        user_response = "END Invalid input."

    return user_response, 200, {'Content-Type': 'text/plain'}


def initiate_paystack_charge(phone_number, amount_ghs):
    url = "https://api.paystack.co/charge"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }

    payload = {
        "email": f"user{phone_number[-6:]}@flap.store",  # dummy email for tracking
        "amount": int(amount_ghs * 100),  # Paystack uses kobo/pesewa
        "currency": "GHS",
        "mobile_money": {
            "phone": phone_number,
            "provider": "mtn"  # or 'vodafone', 'airtel'
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")

