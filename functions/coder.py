import os
from interpreter import interpreter
import json
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key


interpreter.llm.api_key = openai_api_key
interpreter.llm.model = "gpt-3.5-turbo"


interpreter.llm.max_tokens = 1000
interpreter.llm.temperature = 0.7
interpreter.auto_run = True
interpreter.custom_instructions = "Run all pip install commands as pip install -y [package_name]"

def make_query(query, chat):
    q = "Based on the following context:\n" + json.dumps(chat) + "\n\nAnswer the following question:\n" + query
    return q

def coder(query, chat=[], history=[]):
    interpreter.messages = history
    messages = interpreter.chat(make_query(query,chat),stream=False,display=True)
    return messages
