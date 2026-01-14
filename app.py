import streamlit as st
from agent.graph import build_graph
import csv
import os

st.set_page_config(page_title="AI Sales Agent", layout="centered")
st.title("🤖 AI Sales Assistant")

LEADS_CSV = "leads.csv"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = {
        "user_input": "",
        "intent": "",
        "name": None,
        "email": None,
        "company": None
    }

graph = build_graph()

def save_lead(name, email, company):
    if not (name or email):
        return
    file_exists = os.path.isfile(LEADS_CSV)
    with open(LEADS_CSV, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "email", "company"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"name": name or "", "email": email or "", "company": company or ""})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask me anything about AutoStream Pricing or Policies...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    st.session_state.state["user_input"] = user_input

    result = graph.invoke(st.session_state.state)
    st.session_state.state.update(result)

    assistant_response = result.get("response", "").strip()
    intent = st.session_state.state.get("intent", "").lower()

    if intent == "high_intent":
        save_lead(
            st.session_state.state.get("name"),
            st.session_state.state.get("email"),
            st.session_state.state.get("company")
        )

    generic_fallbacks = [
        "how can i assist you further?",
        "may i assist you?",
        "could you please clarify your question?"
    ]

    if not assistant_response or assistant_response.lower() in generic_fallbacks:
        assistant_response = (
            "Here's the information I have about AutoStream pricing and policies:\n\n"
            "- Basic Plan: $29/month, 10 videos, 720p resolution\n"
            "- Pro Plan: $79/month, unlimited videos, 4K resolution, AI captions\n"
            "- No refunds after 7 days\n"
            "- 24/7 support available only on Pro plan\n\n"
            "Feel free to ask me specific questions!"
        )

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    st.rerun()
