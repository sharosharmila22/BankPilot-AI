
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


training_data = [
    ("What is my balance", "balance"),
    ("How much money do I have", "balance"),
    ("Show my available funds", "balance"),
    ("Check my account balance", "balance"),

    ("Show transaction history", "history"),
    ("List previous transactions", "history"),
    ("Show my past payments", "history"),
    ("Display transaction records", "history"),

    ("Check fraud risk", "fraud"),
    ("Is this payment suspicious", "fraud"),
    ("Detect fraudulent transactions", "fraud"),
    ("Is this transfer risky", "fraud"),

    ("I want to transfer money", "transfer"),
    ("Send money to Rahul", "transfer"),
    ("Make a payment", "transfer"),
    ("Transfer funds", "transfer"),

    ("Show customer details", "customer"),
    ("Find customer profile", "customer"),
    ("Look up customer C1001", "customer"),
    ("Show account holder information", "customer"),

    ("Tell me about loans", "loan"),
    ("Show available loan products", "loan"),
    ("Check my loan eligibility", "loan"),
    ("I want an education loan", "loan"),
    ("How can I apply for a personal loan", "loan"),

    ("Hello", "general"),
    ("Hi there", "general"),
    ("What can you do", "general"),
    ("Help me with banking", "general"),
    ("Thank you", "general"),
]

X = [item[0] for item in training_data]
y = [item[1] for item in training_data]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000)),
])

model.fit(X, y)


def get_model_details(user_message):
    probabilities = model.predict_proba([user_message])[0]
    classes = model.classes_
    best_index = probabilities.argmax()

    return {
        "intent": classes[best_index],
        "confidence": float(probabilities[best_index]),
    }


def predict_intent(user_message):
    return get_model_details(user_message)["intent"]
