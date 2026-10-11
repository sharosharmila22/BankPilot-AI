
# Simulated banking tools used by the agents

from agents.customer_agent import get_customer_info
from agents.loan_agent import (
    get_loan_products,
    estimate_loan_eligibility,
)
from database import get_all_transactions


def customer_lookup_tool(customer_id="C1001"):
    return get_customer_info(customer_id)


def transaction_history_tool():
    return get_all_transactions()


def loan_products_tool():
    return get_loan_products()


def loan_eligibility_tool(income, existing_emi, requested_amount):
    return estimate_loan_eligibility(
        income,
        existing_emi,
        requested_amount,
    )
