from flask import Flask, request

app = Flask(__name__)

@app.route("/ussd", methods=["POST"])
def ussd():
    session_id = request.form.get("sessionId", "")
    service_code = request.form.get("serviceCode", "")
    phone_number = request.form.get("phoneNumber", "")
    text = request.form.get("text", "")

    print("Text received:", text)

    if text == "":
        response = "CON Welcome to Flap Market\n1. View Products\n2. Exit"
    elif text == "1":
        response = "END You selected: View Products"
    elif text == "2":
        response = "END Thank you for using Flap"
    else:
        response = "END Invalid input"

    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
