from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Internal session store (RAM-based)
user_sessions = {}

# Initial menu prompt
MAIN_MENU = """MACCI Wallet Terminal

Choose an option:
1. Create Wallet
2. Recover Wallet
3. Mine MACCI
4. Check Balance
5. Send MACCI
6. Exit
"""

@app.route("/terminal", methods=["POST"])
def terminal():
    data = request.get_json()
    user_input = data.get("input", "").strip()
    session_id = "default_user"

    if session_id not in user_sessions:
        user_sessions[session_id] = {"state": "menu", "step": 0, "wallet": None}

    session = user_sessions[session_id]

    # Menu loop
    if session["state"] == "menu":
        if user_input == "1":
            session["state"] = "create"
            return jsonify({"output": "Generating wallet...\n(pretend key/address here)\n" + MAIN_MENU})
        elif user_input == "2":
            session["state"] = "recover"
            return jsonify({"output": "Enter your private key to recover:"})
        elif user_input == "3":
            session["state"] = "mine"
            return jsonify({"output": "Enter your wallet address to mine MACCI:"})
        elif user_input == "4":
            session["state"] = "balance"
            return jsonify({"output": "Enter your wallet address to check balance:"})
        elif user_input == "5":
            session["state"] = "send"
            session["step"] = 0
            return jsonify({"output": "Enter sender wallet address:"})
        elif user_input == "6":
            session["state"] = "menu"
            return jsonify({"output": "Exiting... Goodbye!\n" + MAIN_MENU})
        else:
            return jsonify({"output": "❌ Invalid option.\n" + MAIN_MENU})

    # Recover flow
    elif session["state"] == "recover":
        session["state"] = "menu"
        return jsonify({"output": f"🔑 Wallet recovered for key: {user_input}\n" + MAIN_MENU})

    # Mine flow
    elif session["state"] == "mine":
        session["state"] = "menu"
        return jsonify({"output": f"⛏️ Mining MACCI to {user_input}...\n✅ +10 MACCI\n" + MAIN_MENU})

    # Balance flow
    elif session["state"] == "balance":
        session["state"] = "menu"
        return jsonify({"output": f"💰 Wallet {user_input} has 123 MACCI\n" + MAIN_MENU})

    # Send flow (multi-step input)
    elif session["state"] == "send":
        if session["step"] == 0:
            session["from"] = user_input
            session["step"] += 1
            return jsonify({"output": "Enter recipient wallet address:"})
        elif session["step"] == 1:
            session["to"] = user_input
            session["step"] += 1
            return jsonify({"output": "Enter amount to send:"})
        elif session["step"] == 2:
            session["amount"] = user_input
            session["step"] += 1
            return jsonify({"output": "Enter your private key:"})
        elif session["step"] == 3:
            session["state"] = "menu"
            return jsonify({"output": f"✅ Sent {session['amount']} MACCI from {session['from']} to {session['to']}.\n" + MAIN_MENU})

    return jsonify({"output": "❓ Unknown state.\n" + MAIN_MENU})

if __name__ == "__main__":
    app.run(port=5000)
