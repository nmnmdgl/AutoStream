# agent/memory.py

REQUIRED_FIELDS = ["name", "email", "company"]

def get_missing_fields(state):
    return [f for f in REQUIRED_FIELDS if not state.get(f)]

def extract_details(text, state):
    t = text.lower()

    # Extract email if present (simple check for '@')
    if "@" in text and not state.get("email"):
        state["email"] = text.strip()

    # Extract name if not present and input looks like a name or contains 'name is'
    if not state.get("name"):
        if "name is" in t:
            # Get word(s) after 'name is'
            name_part = text.lower().split("name is")[-1].strip()
            # Take first word as name
            state["name"] = name_part.split()[0].capitalize()
        else:
            # If input short and no keywords, assume it's a name
            if len(text.split()) <= 3 and all(k not in t for k in ["email", "company"]):
                state["name"] = text.strip().capitalize()

    # Extract company if input contains 'company' and not set yet
    if "company" in t and not state.get("company"):
        # Simple heuristic: last word after company
        parts = t.split("company")
        if len(parts) > 1:
            comp = parts[-1].strip().split()[0]
            state["company"] = comp.capitalize()

    return state
