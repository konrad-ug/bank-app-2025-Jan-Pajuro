from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_all()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    return jsonify({"count": registry.count()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.search(pesel)
    if account == None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"name": account.first_name, "surname": account.last_name, "pesel": account.pesel, "balance": account.balance}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    print(f"Update account request: {data}")
    account = registry.search(pesel)
    if account == None:
        return jsonify({"error": "Account not found"}), 404
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.search(pesel)
    if account == None:
        return jsonify({"error": "Account not found"}), 404
    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200
