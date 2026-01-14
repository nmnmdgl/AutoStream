## Running the Project Locally

### Step 1: Clone the Repository

git clone https://github.com/nmnmdgl/AutoStream.git
cd AutoStream
### Step 2: Create Virtual Environment (Python 3.9+)
python -m venv venv

### Step 3: Activate Virtual Environment
Windows:
venv\Scripts\activate

Mac / Linux:
source venv/bin/activate

### Step 4: Install Dependencies
pip install -r requirements.txt

### Step 5: Configure API Keys (.env file)

1. Create a .env file in the root directory:

touch .env


2. Add your API key inside .env:

GOOGLE_API_KEY=your_api_key_here


3. Make sure .env is added to .gitignore:

echo .env >> .gitignore

### Step 6: Run the Application
streamlit run app.py

### Step 7: Open in Browser
http://localhost:8501


# Architecture Explanation

This AI Sales Assistant leverages **LangGraph** for modular conversational state management and **RAG (Retrieval-Augmented Generation)** for answering knowledge-based questions efficiently.

### Why LangGraph / AutoGen?

We chose **LangGraph** because it models conversational flows as a graph of states, allowing clear separation of intent detection, detail extraction, and response generation. This modular design simplifies managing multi-turn dialogues, such as sequential lead capturing, making the system scalable and maintainable.

The AutoGen approach further supports dynamic and extensible conversational agents by defining reusable nodes and edges, facilitating quick updates or feature additions without rewriting the entire logic.

### How State is Managed

State is maintained as a Python dictionary that stores user inputs, detected intents, and extracted details like name, email, and company. This state flows through LangGraph nodes that update it at each step. Using Streamlit’s session state, the conversation persists between messages, enabling smooth multi-turn interactions and consistent user context management.

---

# WhatsApp Deployment: Integration via Webhooks

To integrate the AI Sales Assistant with WhatsApp using Webhooks:

1. **WhatsApp Business API Setup:**

   - Register for WhatsApp Business API and obtain access credentials.
   - Configure a webhook URL that WhatsApp will call for incoming messages.

2. **Webhook Endpoint Implementation:**

   - Build a backend service (e.g., with Flask, FastAPI) to receive POST requests from WhatsApp.
   - Parse incoming messages and sender info from the webhook payload.
   - Forward the message and session context to the AI agent backend (LangGraph-powered logic).
   - Retrieve the agent’s response and format it according to WhatsApp’s message API.

3. **Message Sending:**

   - Use WhatsApp Business API endpoints to send responses back to the user.

4. **Session and State Management:**

   - Track conversation sessions keyed by user phone numbers to maintain state across messages.
   - Store and update user details and conversation context on the backend, mimicking Streamlit session state behavior.

5. **Hosting and Security:**

   - Host webhook on a secure HTTPS server.
   - Implement validation and authentication to verify incoming webhook calls and protect user data.

This setup allows real-time, context-aware conversational AI support directly on WhatsApp.

---
