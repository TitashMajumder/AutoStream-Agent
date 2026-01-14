from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agent.intent import detect_intent
from agent.rag import answer_query
from agent.tools import mock_lead_capture

class AgentState(TypedDict):
     user_input: str
     intent: Optional[str]
     last_topic: Optional[str]
     name: Optional[str]
     email: Optional[str]
     platform: Optional[str]
     pending_field: Optional[str]
     response: str

def intent_node(state: AgentState) -> AgentState:
     if state.get("pending_field"):
          return state
     
     user_input = state.get("user_input", "")
     intent = detect_intent(user_input)
     return {**state, "intent": intent}

def greeting_node(state: AgentState) -> AgentState:
     return {**state, "response": "Hi! I'm your AutoStream assistant. How can I help you today?"}

def product_node(state: AgentState) -> AgentState:
     user_input = state.get("user_input", "").lower().strip()
     # Follow-up handling
     if user_input in ["pro", "pro plan"]:
          state["last_topic"] = "pro"
          return {**state, "response": answer_query("pro")}
     if user_input in ["basic", "basic plan"]:
          state["last_topic"] = "basic"
          return {**state, "response": answer_query("basic")}
     # Normal pricing query
     if "pro" in user_input:
          last_topic = "pro"
     elif "basic" in user_input:
          last_topic = "basic"
     else:
          last_topic = state.get("last_topic")
     
     return {**state, "response": answer_query(user_input), "last_topic": last_topic}

def lead_node(state: AgentState) -> AgentState:
     user_input = state.get("user_input", "").strip()
     name = state.get("name")
     email = state.get("email")
     platform = state.get("platform")
     pending_field = state.get("pending_field")
     if pending_field == "name":
          if user_input:
               return {
                    **state,
                    "response": "What is your email address?",
                    "name": user_input,
                    "pending_field": "email",
                    "user_input": ""
               }
          else:
               return {
                    **state,
                    "response": "Please provide a valid name.",
                    "pending_field": "name",
                    "user_input": ""
               }
     
     elif pending_field == "email":
          if "@" in user_input:
               return {
                    **state,
                    "response": "Which creator platform do you use (YouTube, Instagram, TikTok, etc.)?",
                    "email": user_input,
                    "pending_field": "platform",
                    "user_input": ""
               }
          else:
               return {
                    **state,
                    "response": "Please provide a valid email address.",
                    "pending_field": "email",
                    "user_input": ""
               }
     
     elif pending_field == "platform":
          if user_input:
               mock_lead_capture(name, email, user_input)
               return {
                    **state,
                    "response": "Perfect! You've been successfully added to our lead system.",
                    "platform": user_input,
                    "pending_field": None,
                    "name": None,
                    "email": None,
                    "user_input": ""
               }
          else:
               return {
                    **state,
                    "response": "Please provide a platform name.",
                    "pending_field": "platform",
                    "user_input": ""
               }

     if not name:
          return {
               **state,
               "response": "I'd love to help you get started! What is your name?",
               "pending_field": "name",
               "user_input": ""
          }
     elif not email:
          return {
               **state,
               "response": f"Thanks {name}! What is your email address?",
               "pending_field": "email",
               "user_input": ""
          }
     elif not platform:
          return {
               **state,
               "response": "Which creator platform do you use (YouTube, Instagram, TikTok, etc.)?",
               "pending_field": "platform",
               "user_input": ""
          }

     # Fallback
     return {
          **state,
          "response": "Thank you for your information!",
          "pending_field": None,
          "name": None,
          "email": None,
          "user_input": ""
     }

def route_decision(state: AgentState) -> str:
     if state.get("pending_field"):
          return "lead"
     intent = state.get("intent")
     if intent == "product_inquiry":
          return "product"
     elif intent == "high_intent":
          return "lead"
     return "greeting"

def build_graph():
     graph = StateGraph(AgentState)
     
     # Defining the nodes
     graph.add_node("intent_node", intent_node)
     graph.add_node("greeting", greeting_node)
     graph.add_node("product", product_node)
     graph.add_node("lead", lead_node)
     
     # Flow definition
     graph.set_entry_point("intent_node")
     
     # Conditional logic based on intent
     graph.add_conditional_edges(
          "intent_node",
          route_decision,
          {
               "greeting": "greeting",
               "product": "product",
               "lead": "lead"
          }
     )
     
     # All response nodes lead to END
     graph.add_edge("greeting", END)
     graph.add_edge("product", END)
     graph.add_edge("lead", END)
     
     return graph.compile()