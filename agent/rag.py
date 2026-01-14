import json
import os

def load_knowledge():
     current_dir = os.path.dirname(os.path.abspath(__file__))
     file_path = os.path.join(current_dir, "..", "data", "knowledge_base.json")
     with open(file_path, "r") as f:
          return json.load(f)

def answer_query(query):
     try:
          kb = load_knowledge()
          q = str(query).lower().strip()
          if "pro" in q:
               p = kb["pricing"]["pro"]
               return (
                    f"The Pro Plan costs {p['price']} per month. "
                    f"It includes {p['videos']}, {p['resolution']} resolution, "
                    f"and features like {', '.join(p['features'])}."
               )
          if "basic" in q:
               p = kb["pricing"]["basic"]
               return (
                    f"The Basic Plan costs {p['price']} per month. "
                    f"It includes {p['videos']} with {p['resolution']} resolution."
               )
          if "refund" in q:
               return kb["policies"]["refund"]
          if "support" in q:
               return kb["policies"]["support"]
          return "We have a Basic plan ($29/mo) and a Pro plan ($79/mo). Which one would you like to hear more about?"

     except Exception as e:
          return "I'm having trouble accessing my product information right now."
