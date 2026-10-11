
from agents.intent_model import get_model_details
from agents.account_agent import get_account_balance
from agents.transaction_agent import transfer_money
from agents.fraud_agent import check_transaction
from agents.customer_agent import get_customer_info
from agents.loan_agent import get_loan_products
from database import save_transaction, get_all_transactions


def process_request(user_message):
    details = get_model_details(user_message)
    intent = details["intent"]

    # Extract a demo customer ID when one is mentioned.
    words = user_message.upper().replace(",", " ").split()
    customer_id = next(
        (word for word in words if word.startswith("C") and word[1:].isdigit()),
        "C1001",
    )

    if intent == "balance":
        result = get_account_balance()
        agent = "Account Agent"

    elif intent == "history":
        result = get_all_transactions()
        agent = "Transaction Agent"

    elif intent == "fraud":
        result = (
            "Open Fraud Risk Check and enter an amount. "
            "The demo rules will evaluate its risk."
        )
        agent = "Fraud Detection Agent"

    elif intent == "transfer":
        result = (
            "Open Simulated Transfer to enter the sender, receiver, "
            "and amount. Transfers are simulated only."
        )
        agent = "Transaction Agent"

    elif intent == "customer":
        result = get_customer_info(customer_id)
        agent = "Customer/Banking Agent"

    elif intent == "loan":
        result = get_loan_products()
        agent = "Credit/Loan Agent"

    else:
        result = (
            "I can help with balances, customers, transaction history, "
            "simulated transfers, fraud checks, and loan products."
        )
        agent = "Supervisor Agent"

    return {
        "agent": f"Supervisor Agent -> {agent}",
        "intent": intent,
        "confidence": details["confidence"],
        "result": result,
    }


def process_transfer(sender, receiver, amount):
    if not sender.strip() or not receiver.strip():
        return {
            "status": "failed",
            "message": "Sender and receiver are required.",
        }

    if sender.strip().casefold() == receiver.strip().casefold():
        return {
            "status": "failed",
            "message": "Sender and receiver must be different.",
        }

    if amount <= 0:
        return {
            "status": "failed",
            "message": "Amount must be greater than zero.",
        }

    risk = check_transaction(amount)

    if risk["risk"] == "High":
        return {
            "status": "blocked",
            "agent": "Supervisor Agent -> Fraud Detection Agent",
            "risk": risk["risk"],
            "message": (
                "Transfer blocked by demo risk rules. "
                + risk["message"]
            ),
        }

    result = transfer_money(sender.strip(), receiver.strip(), amount)

    if result["status"] != "success":
        return result

    transaction = result["transaction"].copy()
    transaction["risk"] = risk["risk"]
    save_transaction(transaction)

    return {
        "status": "success",
        "agent": (
            "Supervisor Agent -> Fraud Detection Agent "
            "-> Transaction Agent"
        ),
        "message": "Low-risk simulated transfer recorded.",
        "transaction": transaction,
        "risk": risk["risk"],
    }

