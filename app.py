
import streamlit as st
import pandas as pd
from datetime import datetime

from database import initialize_database, get_all_transactions
from agents.supervisor import process_request, process_transfer
from agents.account_agent import get_account_balance
from agents.fraud_agent import check_transaction
from agents.customer_agent import get_customer_info
from agents.loan_agent import get_loan_products, estimate_loan_eligibility
from agents.llm_agent import generate_natural_language_response


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BankPilot AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "transfer_result" not in st.session_state:
    st.session_state.transfer_result = None


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def safe_get_transactions():
    """Fetch transaction records from the local SQLite database."""
    try:
        records = get_all_transactions()

        if records is None:
            return pd.DataFrame()

        if isinstance(records, pd.DataFrame):
            return records

        if isinstance(records, list):
            return pd.DataFrame(records)

        return pd.DataFrame(records)

    except Exception as error:
        st.error(f"Could not load transactions: {error}")
        return pd.DataFrame()


def display_result(result):
    """Display results from simulated banking tools."""
    if isinstance(result, (dict, list)):
        st.json(result)
    else:
        st.write(result)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🏦 BankPilot AI")
st.sidebar.caption("Multi-Agent Banking Simulation")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Banking Assistant",
        "Account Details",
        "Simulated Transfer",
        "Fraud Risk Check",
        "Transaction History",
        "Customer Lookup",
        "Loan Services",
        "Model Information",
    ],
)

st.sidebar.divider()
st.sidebar.info(
    "Educational demonstration only. "
    "This application does not connect to real bank accounts "
    "or transfer real money."
)


# ==================================================
# 1. DASHBOARD
# ==================================================

if page == "Dashboard":

    st.title("🏦 BankPilot AI Dashboard")
    st.write(
        "Welcome to an AI-powered banking simulation "
        "built using Python, machine learning, and specialized agents."
    )

    account = get_account_balance()

    transactions_df = safe_get_transactions()

    col1, col2, col3 = st.columns(3)

    with col1:
        balance = (
            account.get("balance", 0)
            if isinstance(account, dict)
            else 0
        )
        st.metric("Demo Account Balance", f"₹{balance:,.2f}")

    with col2:
        st.metric("Recorded Transactions", len(transactions_df))

    with col3:
        st.metric("Specialized Agent Types", 5)

    st.divider()

    st.subheader("Available Banking Features")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            - 🤖 AI Banking Assistant
            - 💳 Account Information
            - 💸 Simulated Money Transfer
            - 🛡️ Fraud Risk Detection
            """
        )

    with c2:
        st.markdown(
            """
            - 📜 Transaction History
            - 👤 Customer Lookup
            - 🏠 Loan Services
            - 🧠 Machine Learning Information
            """
        )

    st.warning(
        "All account details, transactions, customer records, "
        "and loan calculations are simulated demo data."
    )


# ==================================================
# 2. AI BANKING ASSISTANT
# ==================================================

elif page == "AI Banking Assistant":

    st.title("🤖 AI Banking Assistant")
    st.write(
        "Enter a banking request. The supervisor agent will "
        "classify the request and route it to the appropriate agent."
    )

    with st.form("banking_assistant_form"):
        user_message = st.text_input(
            "Your banking request",
            placeholder="Example: Show my account balance",
        )

        submitted = st.form_submit_button(
            "Process Request",
            type="primary",
        )

    if submitted:

        if not user_message.strip():
            st.warning("Please enter a banking request.")

        else:
            with st.spinner("Supervisor agent is processing your request..."):

                try:
                    response = process_request(user_message)

                    if not isinstance(response, dict):
                        response = {
                            "result": response,
                            "intent": "unknown",
                            "confidence": 0.0,
                            "agent": "Supervisor Agent",
                        }

                    result = response.get("result", response)

                    st.session_state.chat_history.append(
                        {
                            "request": user_message,
                            "result": result,
                            "intent": response.get("intent", "unknown"),
                            "confidence": response.get("confidence", 0.0),
                            "agent": response.get("agent", "Supervisor Agent"),
                        }
                    )

                    try:
                        answer = generate_natural_language_response(
                            user_message,
                            result,
                        )
                    except Exception as error:
                        answer = (
                            f"Banking tool result: {result}\n\n"
                            f"AI response error: {error}"
                        )

                    st.subheader("AI Assistant Response")
                    st.write(answer)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Predicted Intent",
                            str(response.get("intent", "unknown")).title(),
                        )

                    with col2:
                        confidence = response.get("confidence", 0.0)

                        try:
                            confidence = float(confidence)
                        except (ValueError, TypeError):
                            confidence = 0.0

                        if confidence > 1:
                            confidence /= 100

                        confidence = max(0.0, min(1.0, confidence))

                        st.metric(
                            "Model Confidence",
                            f"{confidence:.1%}",
                        )

                    with col3:
                        st.metric(
                            "Routed Agent",
                            str(response.get("agent", "Supervisor Agent")),
                        )

                    with st.expander("View Raw Banking Tool Result"):
                        display_result(result)

                except Exception as error:
                    st.error(f"Unable to process request: {error}")

    if st.session_state.chat_history:

        st.divider()
        st.subheader("Recent Requests")

        for item in reversed(st.session_state.chat_history[-5:]):
            with st.expander(item["request"]):
                st.write("**Intent:**", item["intent"])
                st.write("**Agent:**", item["agent"])
                st.write("**Tool Result:**")
                display_result(item["result"])


# ==================================================
# 3. ACCOUNT DETAILS
# ==================================================

elif page == "Account Details":

    st.title("💳 Demo Account Details")
    st.write("View the sample account used by the simulation.")

    try:
        account = get_account_balance()

        if isinstance(account, dict):

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Account Information")
                st.write(
                    "**Account Holder:**",
                    account.get("account_holder", "Demo User"),
                )
                st.write(
                    "**Account Number:**",
                    account.get("account_number", "XXXX1234"),
                )
                st.write(
                    "**Currency:**",
                    account.get("currency", "INR"),
                )

            with col2:
                st.subheader("Available Demo Balance")
                balance = account.get("balance", 0)
                st.metric("Balance", f"₹{float(balance):,.2f}")

        else:
            display_result(account)

        st.caption("This is fixed demonstration data, not a real account.")

    except Exception as error:
        st.error(f"Unable to retrieve demo account: {error}")


# ==================================================
# 4. SIMULATED MONEY TRANSFER
# ==================================================

elif page == "Simulated Transfer":

    st.title("💸 Simulated Money Transfer")

    st.warning(
        "Demo only. No actual bank transfer or payment will occur."
    )

    with st.form("transfer_form"):

        sender = st.text_input(
            "Sender",
            value="Demo User",
        )

        receiver = st.text_input(
            "Receiver",
            placeholder="Enter receiver name",
        )

        amount = st.number_input(
            "Transfer Amount (₹)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )

        confirm = st.checkbox(
            "I understand this is a simulated transaction."
        )

        transfer_submitted = st.form_submit_button(
            "Run Simulated Transfer",
            type="primary",
        )

    if transfer_submitted:

        if not sender.strip() or not receiver.strip():
            st.error("Enter both sender and receiver names.")

        elif sender.strip().casefold() == receiver.strip().casefold():
            st.error("Sender and receiver must be different.")

        elif amount <= 0:
            st.error("Transfer amount must be greater than zero.")

        elif not confirm:
            st.warning("Please confirm that this is a simulation.")

        else:
            try:
                with st.spinner("Checking transaction risk..."):

                    risk_result = check_transaction(amount)

                    if isinstance(risk_result, dict):
                        risk_text = str(
                            risk_result.get(
                                "risk",
                                risk_result.get("level", risk_result),
                            )
                        )
                    else:
                        risk_text = str(risk_result)

                    is_high_risk = (
                        "high" in risk_text.casefold()
                        or "block" in risk_text.casefold()
                    )

                    if is_high_risk:
                        st.error(
                            "Transfer was not recorded because the "
                            "risk checker flagged the amount."
                        )
                        display_result(risk_result)

                    else:
                        transfer_result = process_transfer(
                            sender.strip(),
                            receiver.strip(),
                            float(amount),
                        )

                        st.session_state.transfer_result = transfer_result

                        st.subheader("Transfer Result")
                        display_result(transfer_result)

            except Exception as error:
                st.error(f"Transfer processing failed: {error}")


# ==================================================
# 5. FRAUD RISK CHECK
# ==================================================

elif page == "Fraud Risk Check":

    st.title("🛡️ Fraud Risk Check")

    st.write(
        "Evaluate a sample transaction amount using the demo "
        "fraud detection rules."
    )

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0.0,
        value=5000.0,
        step=500.0,
        key="fraud_amount",
    )

    if st.button("Check Fraud Risk", type="primary"):

        try:
            risk_result = check_transaction(float(amount))

            st.subheader("Risk Assessment")
            display_result(risk_result)

            risk_text = str(risk_result).casefold()

            if "high" in risk_text:
                st.error("High risk according to the demo rules.")
            elif "low" in risk_text:
                st.success("Low risk according to the demo rules.")
            else:
                st.info(
                    "Review the returned result. "
                    "This is a simple demonstration, not a production "
                    "fraud detection model."
                )

        except Exception as error:
            st.error(f"Risk check failed: {error}")


# ==================================================
# 6. TRANSACTION HISTORY
# ==================================================

elif page == "Transaction History":

    st.title("📜 Transaction History")

    transactions_df = safe_get_transactions()

    if transactions_df.empty:
        st.info(
            "No transactions are recorded in the SQLite database yet. "
            "Run a simulated transfer first."
        )

    else:
        st.write("Transactions stored by the local database.")

        st.dataframe(
            transactions_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = transactions_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Transaction History (CSV)",
            data=csv_data,
            file_name="bankpilot_transactions.csv",
            mime="text/csv",
        )


# ==================================================
# 7. CUSTOMER LOOKUP
# ==================================================

elif page == "Customer Lookup":

    st.title("👤 Customer Lookup")

    st.write("Search the sample customer records.")

    customer_id = st.text_input(
        "Customer ID",
        value="C1001",
        placeholder="Example: C1001",
    )

    if st.button("Find Customer", type="primary"):

        if not customer_id.strip():
            st.warning("Enter a customer ID.")

        else:
            try:
                customer = get_customer_info(customer_id.strip())

                st.subheader("Customer Information")
                display_result(customer)

            except Exception as error:
                st.error(f"Customer lookup failed: {error}")

    st.caption("Only predefined demo customer records are available.")


# ==================================================
# 8. LOAN SERVICES
# ==================================================

elif page == "Loan Services":

    st.title("🏠 Loan Services")

    st.write("Explore sample loan products and a demo eligibility estimate.")

    try:
        loan_products = get_loan_products()

        st.subheader("Available Loan Products")
        display_result(loan_products)

    except Exception as error:
        st.error(f"Could not load loan products: {error}")

    st.divider()
    st.subheader("Demo Loan Eligibility Estimator")

    with st.form("loan_eligibility_form"):

        monthly_income = st.number_input(
            "Monthly Income (₹)",
            min_value=0.0,
            value=30000.0,
            step=1000.0,
        )

        existing_monthly_emi = st.number_input(
            "Existing Monthly EMI (₹)",
            min_value=0.0,
            value=0.0,
            step=500.0,
        )

        requested_amount = st.number_input(
            "Requested Loan Amount (₹)",
            min_value=0.0,
            value=100000.0,
            step=10000.0,
        )

        loan_submitted = st.form_submit_button(
            "Estimate Eligibility",
            type="primary",
        )

    if loan_submitted:

        if monthly_income <= 0:
            st.error("Monthly income must be greater than zero.")

        elif existing_monthly_emi > monthly_income:
            st.warning(
                "Existing EMI exceeds monthly income. "
                "Please verify the entered figures."
            )

        elif requested_amount <= 0:
            st.error("Requested loan amount must be greater than zero.")

        else:
            try:
                eligibility = estimate_loan_eligibility(
                    float(monthly_income),
                    float(existing_monthly_emi),
                    float(requested_amount),
                )

                st.subheader("Eligibility Estimate")
                display_result(eligibility)

            except Exception as error:
                st.error(f"Eligibility calculation failed: {error}")

    st.caption(
        "This estimate is for demonstration only and is not a real "
        "credit assessment or loan approval."
    )


# ==================================================
# 9. MODEL INFORMATION
# ==================================================

elif page == "Model Information":

    st.title("🧠 AI and Multi-Agent Architecture")

    st.write(
        "BankPilot AI demonstrates how a supervisor can route requests "
        "to specialized banking agents."
    )

    st.subheader("Architecture")

    st.code(
        """
User Request
     |
     v
Supervisor / Orchestrator Agent
     |
     v
Intent Classification Model
     |
     +----> Account Agent
     |
     +----> Transaction Agent
     |
     +----> Fraud Detection Agent
     |
     +----> Customer Agent
     |
     +----> Loan Agent
     |
     v
Simulated Banking Tools / SQLite
     |
     v
Optional Gemini LLM Response
     |
     v
Streamlit User Interface
        """,
        language="text",
    )

    st.subheader("Technology Stack")

    technologies = {
        "Component": [
            "Programming Language",
            "User Interface",
            "Intent Classification",
            "Machine Learning",
            "Database",
            "Natural Language Generation",
        ],
        "Technology": [
            "Python",
            "Streamlit",
            "TF-IDF and Logistic Regression",
            "Scikit-learn",
            "SQLite",
            "Google Gemini API (optional)",
        ],
    }

    st.dataframe(
        pd.DataFrame(technologies),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Specialized Agents")

    st.markdown(
        """
        1. **Account Agent:** returns sample account details.
        2. **Transaction Agent:** handles simulated transactions.
        3. **Fraud Agent:** evaluates transactions using demo rules.
        4. **Customer Agent:** looks up predefined customer records.
        5. **Loan Agent:** lists loan products and estimates eligibility.
        6. **Supervisor Agent:** classifies requests and selects a route.
        """
    )

    st.warning(
        "The intent classifier is a machine-learning model, while Gemini "
        "is the optional large language model. The banking data and tools "
        "are simulated; this is not a production banking system."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    f"BankPilot AI | Multi-Agent Banking Simulation | "
    f"Session date: {datetime.now().strftime('%d-%m-%Y')}"
)
