import os
import json
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key

from openai import OpenAI


def make_query(query, chat):
    q = "Based on the following context:\n" + json.dumps(chat) + "\n\nAnswer the following question:\n" + query
    return q

class Coder():
    def __init__(self, project_name, custom_instructions=""):
        import interpreter
        self.chat = []
        self.history = []
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai = OpenAI(api_key=openai_api_key)
        self.interpreter = interpreter.interpreter
        self.interpreter.llm.api_key = self.openai_api_key
        self.interpreter.llm.model = "gpt-4-turbo"
        self.interpreter.llm.temperature = 0
        self.interpreter.auto_run = True
        self.interpreter.llm.context_window = 10000
        self.interpreter.llm.max_tokens = 4096
        self.project_name = project_name
        folder = os.path.join(os.getcwd(), "data")
        self.path = os.path.join(folder, project_name)
        self.interpreter.chat(f"Check if the directory {self.path} exists. If not create the directory")
        ci = "Run all pip install commands as pip install -y [package_name]."
        self.interpreter.custom_instructions = custom_instructions + ci # + f"Write code(python/c++ etc. code only) in {self.path} in new files. Do not write cli commands or any other information."
    
    def make_query(self, query, context):
        q = "Based on the following context:\n" + context + "\n\nAnswer the following question:\n" + query
        return q
    
    def add_chat(self, chat):
        self.chat.append(chat)
    def add_history(self, history):
        self.history.append(history)
    def code(self, query, context):
        q = make_query(query, context)
        messages = self.interpreter.chat(q, stream=False, display=True)
        self.add_history(messages)
        self.interpreter.chat(f"Write this code in a new file that does not already exist files in the {self.path} directory. Use proper formatting and no '\n's")
        return messages
    def parse_output(self, messages):
        response = {"code":[], "output":[], "message":[]} # code, console, message
        for message in messages:
            if message["type"] == "code":
                response["code"].append({"code":message["content"],"language":message["format"]})
            elif message["type"] == "console":
                response["output"].append(message["content"])
            elif message["type"] == "message":
                response["message"].append(message["content"])
        return response
    def generate_summary(self, parsed_output):
        code = parsed_output["code"]
        output = parsed_output["output"]
        message = parsed_output["message"]
        prompt = f"""
        Given the following Open Interpreter Response, summarise its initial plan, the actions taken and the conclusion in concise points.
        Code Output:
        {output}
        Interpreter Code:
        {code}
        Interpreter Message:
        {message}
        """
        summary = self.openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": prompt}
            ],
            temperature = 0.7
        )
        return summary.choices[0].message.content
    
if __name__ == "__main__":
    c = Coder("1")
    sample_message = {
        {"role": "assistant", "type": "code", "format": "python", "start": True},
        {"role": "assistant", "type": "code", "format": "python", "content": "34"},
        {"role": "assistant", "type": "code", "format": "python", "content": " /"},
        {"role": "assistant", "type": "code", "format": "python", "content": " "},
        {"role": "assistant", "type": "code", "format": "python", "content": "24"},
        {"role": "assistant", "type": "code", "format": "python", "end": True}
    }
