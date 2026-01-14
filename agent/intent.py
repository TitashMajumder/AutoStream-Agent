def detect_intent(user_input, state=None):
     # Standardize input
     if isinstance(user_input, dict):
          user_input = user_input.get("user_input", "")
     text = str(user_input).lower().strip()
     if state and state.get("pending_field"):
          return "high_intent"
     
     # Rule 1: High-Intent
     high_intent_keywords = ["sign up", "try", "buy", "subscribe", "want pro", "get started", "onboard"]
     if any(word in text for word in high_intent_keywords):
          return "high_intent"

     # Rule 2: Product Inquiry
     product_keywords = ["price", "pricing", "cost", "plan", "basic", "pro", "feature", "resolution", "video", "refund", "support"]
     if any(word in text for word in product_keywords):
          return "product_inquiry"

     # Rule 3: Greetings
     if any(word in text for word in ["hi", "hello", "hey", "greet"]):
          return "greeting"

     return "greeting"