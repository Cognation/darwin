import os
import json
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key

from openai import OpenAI
openai = OpenAI(api_key=openai_api_key)

def make_query(query, chat):
    q = "Based on the following context:\n" + json.dumps(chat) + "\n\nAnswer the following question:\n" + query
    return q

class Coder():
    def __init__(self):
        import interpreter
        self.chat = []
        self.history = []
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.interpreter = interpreter.interpreter
        self.interpreter.llm.api_key = self.openai_api_key
        self.interpreter.llm.model = "gpt-3.5-turbo"
        self.interpreter.llm.temperature = 0.7
        self.interpreter.auto_run = True
        self.interpreter.custom_instructions = "Run all pip install commands as pip install -y [package_name]"
    
    def make_query(self, query):
        q = "Based on the following context:\n" + json.dumps(self.chat) + "\n\nAnswer the following question:\n" + query
        return q
    
    def add_chat(self, chat):
        self.chat.append(chat)
    def add_history(self, history):
        self.history.append(history)
    def code(self, query):
        q = make_query(query, self.chat)
        messages = self.interpreter.chat(q, stream=False, display=True)
        self.add_history(messages)
        return messages
    def parse_output(self, messages):
        response = {"code":[], "output":[], "message":[]} # code, console, message
        for message in messages:
            if message["type"] == "code":
                response["code"].append(message["content"])
            elif message["type"] == "console":
                response["output"].append(message["content"])
            elif message["type"] == "message":
                response["message"].append(message["content"])
        return response
    def generate_summary(self, parsed_output):
        code = "\n".join(parsed_output["code"])
        output = "\n".join(parsed_output["output"])
        message = "\n".join(parsed_output["message"])
        prompt = """
        Given the following Open Interpreter Response, summarise its initial plan, it actions and the conclusion in concise points.
        Code Output:
        """ + output + """
        Interpreter Code:
        """ + code + """
        Interpreter Message:
        """ + message + """ 
        """
        summary = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": prompt}
            ],
            temperature = 0.7
        )
        return summary 