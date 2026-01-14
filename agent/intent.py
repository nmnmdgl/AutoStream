INTENTS = {
    "pricing": ["price", "cost", "charges", "fee"],
    "high_intent": ["buy", "purchase", "demo", "trial", "subscribe"],
    "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "morning"],
    "chitchat": ["how are you", "what's up", "how is it going"]
}

def detect_intent(text):
    text = text.lower()
    for intent, keywords in INTENTS.items():
        if any(k in text for k in keywords):
            return intent
    return "general"
