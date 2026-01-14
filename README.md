##AutoStream – Agentic Lead Qualification System
####📌 Overview

AutoStream is a production-style agentic system that simulates how AI sales and support agents operate on social platforms.
The agent understands user intent, answers pricing and policy questions accurately, and captures leads through a controlled, multi-step workflow.

This project was built as part of the Machine Learning Intern Assignment and focuses on agent design, not chatbot-style conversation.

✨ Key Capabilities

Intent classification (greeting, product inquiry, high intent)

Deterministic RAG using a local knowledge base

Multi-turn conversation state management

Safe and gated tool execution for lead capture

Explicit agent orchestration using LangGraph

🧠 Architecture Overview

The system is implemented using LangGraph, which models the agent as a state machine instead of a linear chat loop.
Each user message updates a shared state that is passed across nodes responsible for intent detection, product responses, and lead qualification.

Pricing and policy answers are generated using a local JSON knowledge base, ensuring factual correctness and eliminating hallucinations.
When high intent is detected, the agent transitions into a structured lead qualification flow, collecting user details across multiple turns.

Tool execution (lead capture) is strictly gated and triggered only when all required information is present in the state.
This architecture mirrors real-world AI agents used in sales automation rather than open-ended chatbots.

The intent detection module is LLM-agnostic and currently implemented deterministically. During development, this approach was chosen to ensure reliability under API quota constraints, while keeping the workflow fully compatible with LLM-based intent modules such as GPT-4o-mini, Gemini 1.5 Flash, or Claude 3 Haiku.

🧩 Design Decisions

LangGraph over simple loops: Enables explicit control over state, routing, and termination.

Deterministic RAG: Prevents hallucinations for pricing and policy information.

Tool gating: Ensures backend actions are executed only when state is complete.

LLM-agnostic intent layer: Allows easy swap to any supported LLM without workflow changes.

🗂️ Project Structure
AutoStream-Agent/
│
├── agent/
│   ├── graph.py        # LangGraph workflow
│   ├── intent.py       # Intent detection
│   ├── rag.py          # RAG over local knowledge base
│   └── tools.py        # Lead capture tool
│
├── data/
│   └── knowledge_base.json
│
├── main.py             # Application entry point
├── requirements.txt
└── README.md

📚 Knowledge Base (RAG)

The agent uses a local JSON file containing:

Pricing

Basic Plan – $29/month
10 videos/month, 720p resolution

Pro Plan – $79/month
Unlimited videos, 4K resolution, AI captions, priority support

Policies

No refunds after 7 days

24/7 support available on Pro plan only

▶️ How to Run Locally
# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows


(macOS/Linux: source venv/bin/activate)

# Install dependencies
pip install -r requirements.txt

# Run the agent
python main.py

💬 Example Interaction
User: hi
Agent: Hi! I'm your AutoStream assistant. How can I help you today?

User: what is the pro price
Agent: The Pro Plan costs $79/month. It includes unlimited videos, 4K resolution, and AI captions.

User: I want to get started
Agent: I'd love to help you get started! What is your name?

User: Titash
Agent: What is your email address?

User: titash@gmail.com
Agent: Which creator platform do you use?

User: YouTube
Lead captured successfully: Titash, titash@gmail.com, YouTube

🔐 Why This Is Not a Chatbot

The agent maintains explicit conversation state

Routing is deterministic, not free-form

Tool execution is validated and gated

Responses depend on multi-turn context, not only the last message

This design aligns with real-world AI agents used in production systems.

📱 WhatsApp Deployment Approach

The agent can be integrated with WhatsApp using the WhatsApp Business API. Incoming messages trigger a webhook that forwards the message to the backend. Conversation state can be stored per phone number, enabling multi-turn interactions. Responses are sent back using the WhatsApp Send Message API.

⚠️ Failure Handling

Unknown or ambiguous inputs fall back to safe conversational prompts

Lead capture is prevented unless all required fields are present

Knowledge base access failures return graceful error messages

🔮 Future Improvements

Replace deterministic intent detection with LLM-based classification

Persist conversation state using Redis or a database

Add confidence-based lead scoring

🛠️ Tech Stack

Python 3.9+

LangGraph (agent orchestration)

Deterministic intent detection

JSON-based RAG

Modular, LLM-agnostic design

✅ Evaluation Coverage
Requirement	Status
Intent detection	✅
RAG	✅
State management	✅
Tool execution	✅
Agentic workflow	✅
🏁 Final Notes

This project demonstrates a real-world agent architecture, focusing on reliability, state management, and controlled actions rather than free-form conversation.
