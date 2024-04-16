import os
from interpreter import interpreter
from dotenv import load_dotenv
import json
interpreter.llm.model = "gpt-3.5-turbo"

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

interpreter.llm.max_tokens = 1000
interpreter.llm.temperature = 0.7
interpreter.auto_run = True
interpreter.custom_instructions = "Your name is ENIGMA."

def make_query(query, chat):
    q = "Based on the following context:\n" + json.dumps(chat) + "\n\nAnswer the following question:\n" + query
    return q

def coder(query, chat=[], history=[]):
    interpreter.messages = history
    messages = interpreter.chat(make_query(query,chat),stream=False,display=True)
    return messages
