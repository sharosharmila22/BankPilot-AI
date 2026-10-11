
# Simulated customer/banking agent

CUSTOMERS = {
    "C1001": {
        "customer_id": "C1001",
        "name": "Demo User",
        "account_type": "Savings",
        "account_status": "Active",
        "branch": "Chennai",
    },
    "C1002": {
        "customer_id": "C1002",
        "name": "Rahul",
        "account_type": "Current",
        "account_status": "Active",
        "branch": "Coimbatore",
    },
}


def get_customer_info(customer_id="C1001"):
    """Retrieve a simulated customer profile."""
    customer_id = customer_id.strip().upper()

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return {
            "success": False,
            "message": "Customer not found in the demo database.",
        }

    return {
        "success": True,
        "customer": customer,
    }


def list_customers():
    """Return all simulated customer profiles."""
    return list(CUSTOMERS.values())
