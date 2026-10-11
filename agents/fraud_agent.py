
def check_transaction(amount):
    """Basic rule-based demo fraud screening."""

    if amount <= 0:
        return {
            "risk": "High",
            "message": "Invalid transaction amount."
        }

    if amount >= 100000:
        return {
            "risk": "High",
            "message": "Large transaction flagged for review."
        }

    return {
        "risk": "Low",
        "message": "No demo risk rule triggered."
    }
