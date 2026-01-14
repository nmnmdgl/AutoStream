# agent/graph.py

from langgraph.graph import StateGraph
from agent.intent import detect_intent
from agent.memory import get_missing_fields, extract_details
from agent.tools import lead_capture_tool
from agent.rag import setup_vectorstore, query_rag

vectordb = setup_vectorstore()

def intent_node(state):
    # If currently collecting lead details (some missing fields), force high_intent
    missing = get_missing_fields(state)
    if missing and state.get("intent") == "high_intent":
        # Continue high_intent until all details collected
        print("[DEBUG] Continuing high_intent because details missing")
        return state

    # Otherwise, detect intent normally
    detected_intent = detect_intent(state["user_input"])
    state["intent"] = detected_intent
    print(f"[DEBUG] intent_node: Detected intent = {detected_intent}")
    return state

def conversation_node(state):
    state = extract_details(state["user_input"], state)
    print(f"[DEBUG] conversation_node: After extract_details: {state}")

    intent = state["intent"]
    print(f"[DEBUG] conversation_node: intent = {intent}, user_input = {state['user_input']}")

    if intent == "pricing":
        answer = query_rag(vectordb, state["user_input"])
        print(f"[DEBUG] conversation_node: RAG answer = {answer}")
        state["response"] = f"{answer}\n\nWould you like a demo?"
        return state

    if intent == "high_intent":
        missing = get_missing_fields(state)
        if missing:
            state["response"] = f"May I know your {missing[0]}?"
            return state
        # All details collected, capture lead
        state["response"] = lead_capture_tool({
            "name": state["name"],
            "email": state["email"],
            "company": state["company"]
        })
        return state

    if intent == "greeting":
        state["response"] = "Hello! How can I help you today?"
        return state

    if intent == "chitchat":
        state["response"] = "I'm doing great, thanks for asking! How can I assist you?"
        return state

    # fallback response
    state["response"] = (
        "I'm here to help with AutoStream pricing, plans, and demos. What would you like to know?"
    )
    return state

def build_graph():
    graph = StateGraph(dict)
    graph.add_node("intent", intent_node)
    graph.add_node("conversation", conversation_node)
    graph.set_entry_point("intent")
    graph.add_edge("intent", "conversation")
    return graph.compile()
