
# Simulated credit and loan agent

LOAN_PRODUCTS = [
    {
        "name": "Personal Loan",
        "maximum_demo_amount": 500000,
        "illustrative_annual_interest_rate": 12.0,
    },
    {
        "name": "Education Loan",
        "maximum_demo_amount": 1000000,
        "illustrative_annual_interest_rate": 8.5,
    },
    {
        "name": "Home Loan",
        "maximum_demo_amount": 2500000,
        "illustrative_annual_interest_rate": 8.0,
    },
]


def get_loan_products():
    """Retrieve simulated loan products."""
    return LOAN_PRODUCTS


def estimate_loan_eligibility(monthly_income, existing_monthly_emi,
                              requested_amount):
    """Produce a simple illustrative loan estimate, not a bank decision."""

    if monthly_income <= 0 or existing_monthly_emi < 0:
        return {
            "status": "Invalid input",
            "message": "Enter positive income and non-negative existing EMI.",
        }

    if requested_amount <= 0:
        return {
            "status": "Invalid input",
            "message": "Requested loan amount must be greater than zero.",
        }

    if existing_monthly_emi > monthly_income:
        return {
            "status": "Not eligible under demo rules",
            "message": "Existing EMI exceeds monthly income.",
            "estimated_available_monthly_income": 0,
        }

    # Demo affordability rule: existing EMI plus new EMI should not
    # exceed 40% of monthly income.
    available_for_emi = max(
        0,
        monthly_income * 0.40 - existing_monthly_emi
    )

    # Approximate 5-year EMI at an illustrative 12% annual rate.
    monthly_rate = 0.12 / 12
    months = 60

    estimated_emi = (
        requested_amount * monthly_rate
        / (1 - (1 + monthly_rate) ** (-months))
    )

    eligible = estimated_emi <= available_for_emi

    return {
        "status": (
            "Eligible under demo rules"
            if eligible
            else "Not eligible under demo rules"
        ),
        "requested_amount": requested_amount,
        "estimated_monthly_emi": round(estimated_emi, 2),
        "estimated_available_monthly_income": round(
            available_for_emi, 2
        ),
        "message": (
            "This is only an illustrative estimate, not an actual "
            "lending decision or loan approval."
        ),
    }
