from agent.graph import build_graph

app = build_graph()

state = {
     "user_input": "",
     "intent": None,
     "last_topic": None,
     "name": None,
     "email": None,
     "platform": None,
     "pending_field": None,
     "response": ""
}

while True:
     user_input = input("User: ").strip()
     if not user_input:
          continue
     
     # Set the user input in state
     state["user_input"] = user_input
     result = app.invoke(state)
     if isinstance(result, dict):
          state.update(result)
     
     # Display response
     print(f"Agent: {state['response']}\n")