
from datetime import datetime

# Demo transaction history
transactions = []


def transfer_money(sender, receiver, amount):
    """Simulate a transfer without moving real money."""

    if amount <= 0:
        return {
            "status": "failed",
            "message": "Amount must be greater than zero."
        }

    transaction = {
        "sender": sender,
        "receiver": receiver,
        "amount": round(float(amount), 2),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "status": "simulated"
    }

    transactions.append(transaction)

    return {
        "status": "success",
        "message": "Demo transfer simulated successfully!",
        "transaction": transaction
    }


def get_transaction_history():
    """Return all simulated transactions."""
    return transactions
