
# BankPilot AI
## Simulated Real-Time Banking Architecture with Multi-Agent Automation

### 1. Project Overview

BankPilot AI is an AI-powered banking simulation that demonstrates how
multiple specialized agents collaborate to process natural-language
banking requests.

A Supervisor/Orchestrator Agent classifies user requests and routes
them to the appropriate banking agent. The application uses simulated
banking data and a Streamlit interface.

This project is developed as a technical assignment and does not
connect to real banking systems or transfer actual money.

### 2. Objectives

- Demonstrate multi-agent architecture.
- Route user requests using an intent classification model.
- Simulate common banking operations.
- Evaluate transaction risk using demo rules.
- Demonstrate customer lookup and loan estimation.
- Generate natural-language responses using an optional LLM.

### 3. Technology Stack

- Python
- Streamlit
- Scikit-learn
- TF-IDF and Logistic Regression
- SQLite
- Pandas
- Google Gemini API (optional LLM integration)

### 4. System Architecture

User
  |
  v
Streamlit User Interface
  |
  v
Supervisor / Orchestrator Agent
  |
  v
Intent Classification Model
  |
  +--> Account Agent
  |
  +--> Transaction Agent
  |
  +--> Fraud Detection Agent
  |
  +--> Customer Agent
  |
  +--> Loan Agent
  |
  v
Simulated Banking Tools and SQLite Database
  |
  v
Optional Gemini LLM Response

### 5. Main Features

1. AI Banking Assistant
2. Demo Account Details
3. Simulated Money Transfer
4. Fraud Risk Assessment
5. Transaction History
6. Customer Lookup
7. Loan Product Information
8. Demo Loan Eligibility Estimator
9. Model and Architecture Information

### 6. Project Structure

BankPilot_Ai/
|
|-- app.py
|-- database.py
|-- bankpilot.db
|-- README.md
|
|-- agents/
    |-- __init__.py
    |-- supervisor.py
    |-- intent_model.py
    |-- account_agent.py
    |-- transaction_agent.py
    |-- fraud_agent.py
    |-- customer_agent.py
    |-- loan_agent.py
    |-- banking_tools.py
    |-- llm_agent.py

The database file may be created automatically when the application runs.

### 7. Installation

Install Python 3.11 or a compatible Python version.

Open a terminal in the project directory and install dependencies:

    python -m pip install streamlit pandas scikit-learn google-genai

### 8. Run the Application

Execute:

    python -m streamlit run app.py

Open the local URL displayed in the terminal.

### 9. Optional Gemini Configuration

Create an API key through Google AI Studio:

https://aistudio.google.com/apikey

In PowerShell, set the key for the current terminal session:

    $env:GEMINI_API_KEY="YOUR_API_KEY_HERE"

Then run the application in the same terminal.

Never commit API keys or other secrets to source control.

### 10. Sample Test Requests

- What is my account balance?
- Show my transaction history.
- Check the fraud risk for 50000.
- Find customer C1001.
- Show available loan products.

Use the application's dedicated pages to test transfers, risk checks,
customer lookup, loan estimation, and transaction history.

### 11. Limitations

- Account and customer data are simulated.
- Transfers do not move real money.
- Fraud checking uses demonstration rules and is not a production
  fraud detection system.
- Loan estimates are not real credit decisions or approvals.
- Gemini requires a valid API key and network access.
- SQLite stores local application records.

### 12. Conclusion

BankPilot AI demonstrates how an orchestrator, machine-learning
intent classification, specialized agents, simulated banking tools,
a local database, and an optional large language model can be
combined in a single application.

The system is intended for educational demonstration and is not
designed for real banking transactions.
