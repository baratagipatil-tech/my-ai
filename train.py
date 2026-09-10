from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Training questions
questions = [
    "hello",
    "hi",
    "hey",
    "good morning",

    "what is python",
    "tell me about python",
    "explain python",

    "what is machine learning",
    "explain machine learning",
    "what is ML"
]

# Labels: what each question means
labels = [
    "greeting",
    "greeting",
    "greeting",
    "greeting",

    "python",
    "python",
    "python",

    "machine_learning",
    "machine_learning",
    "machine_learning"
]

# Convert text into numbers
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(questions)

# Create the ML model
model = LogisticRegression()

# Train the model
model.fit(X, labels)

print("Model trained successfully!")

# Test the model
test_question = input("Ask something: ")

test_X = vectorizer.transform([test_question])

prediction = model.predict(test_X)

print("AI thinks this is:", prediction[0])