import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pyttsx3



# Training data — some sarcastic, some not
data = [
    "Oh great, another rainy day",
    "I absolutely love getting stuck in traffic",
    "My phone battery died again, awesome!",
    "Wow, I got a promotion!",
    "I can’t believe I won the lottery",
    "Perfect, spilled coffee on my laptop",
    "Lovely, the printer jammed again",
    "Yay, Monday mornings!",
    "This pizza is amazing",
    "I’m so excited to pay bills"
]

labels = [1, 1, 1, 0, 0, 1, 1, 1, 0, 1]  # 1 = Sarcastic, 0 = Genuine

# Vectorize text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data)

# Train model
model = MultinomialNB()
model.fit(X, labels)

funny_replies = [
    "Translation: You actually hate that 😏",
    "Someone’s being sarcastic again!",
    "Tell me how you *really* feel 😂",
    "Exactly what i needed today",
    "best time of the month, obviously",
    "So much enthusiasm, wow!"
]
engine = pyttsx3.init()
engine.say(random.choice(funny_replies))
engine.runAndWait()

# Simple loop
print("🤖 Moodify: Sarcasm Translator v1.0")
print("Type something (or 'exit' to quit):")

while True:
    user_input = input("> ")
    if user_input.lower() == "exit":
        print("Goodbye, realist!")
        break

    X_test = vectorizer.transform([user_input])
    pred = model.predict(X_test)[0]

    if pred == 1:
        print(random.choice(funny_replies))
    else:
        print("That sounds genuine 🙂")
