import os
import json
from dotenv import load_dotenv
load_dotenv()

from aider.io import InputOutput
from aider.models import Model
from aider.repomap import RepoMap
import re

from openai import OpenAI


def make_query(query, chat, map, cwd):
    q = "Based on the following context:\n" + json.dumps(chat) + f" and the current folder tree(which shows the different files and relevant classes, can be used to analyze/edit existing codebase) : {map}\n\Answer and Code the following query:\n" + query + "Use {cwd} as the current working directory."
    return q

class Coder():
    def __init__(self, project_name, custom_instructions=""):
        import interpreter
        self.chat = []
        self.history = []
        self.errors = 0
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4-turbo"
        self.openai = OpenAI(api_key=self.openai_api_key)
        self.interpreter = interpreter.interpreter
        self.interpreter.llm.api_key = self.openai_api_key
        self.interpreter.llm.model = self.model
        self.interpreter.llm.temperature = 0
        self.interpreter.auto_run = True
        self.interpreter.llm.context_window = 8192
        self.interpreter.llm.max_tokens = 4096
        self.project_name = project_name
        folder = os.path.join(os.getcwd(), "data")
        self.path = os.path.join(folder, project_name)
        ci = f"""
        You are the world's best professional programmer, you task is to write end-to-end running code for the query provided below.

        Important Instructions:
        # Your current working directory is {self.path}, no work is to be done outside this folder including repo clones!
        # You will be given access to a folder tree which shows the different files and relevant classes, within your CWD directory, that can be used to analyze/edit the existing codebase.
        # You cannot ask the user for any input, any input required should be hardcoded.
        # You do not have access to run servers on ports, comment out any main commands to host servers after writing the code.

        Follow each instruction else you will be fined $1000 for each instruction missed.
        """
        self.interpreter.custom_instructions = ci
        self.repo_map = ""
        # self.interpreter.chat(f"Check if the directory {self.path} exists. If not create the directory")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"Directory created: {self.path}")
        else:
            print(f"Directory already exists: {self.path}")

        # ci = f"Very Important : Your working directory is {self.path}, no work is to be done outside this folder including repo clones! . Run all pip install commands as pip install -y [package_name]. Write end-to-end code in proper code format, not as text."
        # self.interpreter.custom_instructions = ci + custom_instructions # + f"Write code(python/c++ etc. code only) in {self.path} in new files. Do not write cli commands or any other information."
        self.load_history()
        print("path : ",self.path)

    def make_query(self, query, context, map, cwd):
        # q = "Based on the following context:\n" + context + f" and the current folder tree(which shows the different files and relevant classes, can be used to analyze/edit existing codebase) : {map}\n\Answer and Code the following query:\n" + query + f"Use {cwd} as the current working directory."
        q = f"""
        Given the following context : {context} and the current folder tree(which shows the different files and relevant classes, can be used to analyze/edit existing codebase) : {map}
        Answer and Code the following query : {query}
        Use {cwd} as the current working directory for all operations.
        """
        return q
    
    def add_chat(self, chat):
        self.chat.append(chat)

    def add_history(self, chunk):
        self.history.append(chunk)

    def save_history(self):
        with open(os.path.join(self.path, "history.json"), "w") as f:
            json.dump(self.interpreter.history, f)

    def load_history(self):
        if not os.path.exists(os.path.join(self.path, "history.json")):
            with open(os.path.join(self.path, "history.json"), "w") as f:
                json.dump([], f)
        with open(os.path.join(self.path, "history.json"), "r") as f:
            self.history = json.load(f)
            self.interpreter.history = self.history

    def code(self, query, context):
        self.get_repo_map()
        q = self.make_query(query, context, self.repo_map, self.path)
        temp = ""
        messages = []
        for chunk in self.interpreter.chat(q, stream=True, display=True):
            if(type(chunk) == str):
                pass
            self.add_history(chunk)
            messages.append(chunk)
            if 'start' in chunk:
                key = chunk["type"]
            elif 'end' in chunk:
                # if(key=="code"):
                #     content = temp
                #     # append to file code.py
                #     with open(os.path.join(self.path, "code.py"), "a") as f:
                #         f.write(content)
                "UNCOMMENT"
                # yield json.dumps({key:temp}).encode("utf-8") + b"\n"
                temp = ""
            else:
                if 'format' in chunk and chunk["format"] == "active_line":
                    pass
                if 'content' in chunk:
                    if(type(chunk['content'])==dict):
                        chunk = chunk['content']
                    if "key" == "console" and chunk["format"] == "output" and "Error" in chunk["content"]:
                        self.errors += 1
                        if self.errors > 2:
                            # self.interpreter.chat("Too many errors. Exiting.")
                            self.summary = "Got errors while writing code, here is a summary of what was done.\n" + self.generate_summary(self.parse_output(messages)) + "Recommend calling Web Search."
                            "UNCOMMENT"
                            # yield json.dumps({"exit":True}).encode("utf-8") + b"\n"
                            break
                    temp += str(chunk["content"])
        # print("Message : ",messages)
        self.interpreter.chat(f"If required, write the code from your history in a new file that does not already exist in the {self.path} directory with open, else skip. Use proper formatting and no '\n's")
        self.save_history()
        self.summary = self.generate_summary(self.parse_output(messages))

    def parse_output(self, messages):
        response = {"code":[], "output":[], "message":[]} # code, console, message
        for message in messages:
            try:
                # if message["type"] == "code":
                #     response["code"].append(message["content"])
                # if message["type"] == "console":
                #     response["output"].append(message["content"])
                if message["type"] == "message":
                    response["message"].append(message["content"])
            except:
                pass
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
        Write in plain text.
        """
        summary = self.openai.chat.completions.create(
            model = "gpt-4-turbo",
            messages = [
                {"role": "system", "content": prompt}
            ],
            temperature = 0.7
        )
        return summary.choices[0].message.content
    
    def get_repo_map(self):
        model = Model("gpt-4-turbo")
        io = InputOutput()
        dir =  os.path.join(os.getcwd(), "data", self.project_name)
        files = []
        excl = [
            r'^\.',
            r'^\.git*',
            r'^__pycache__',
            r'history.json'
        ]

        for root, _, file in os.walk(dir):
            for f in file:
                full_path = os.path.join(root, f)
                path_components = os.path.normpath(full_path).split(os.sep)
                if not any(re.search(pattern, component) for component in path_components for pattern in excl):
                    files.append(full_path)
        repoMap = RepoMap(main_model=model, root=dir, io=io)
        self.repo_map = repoMap.get_repo_map([],files)
        print("Repo Map : ",self.repo_map)

    
if __name__ == "__main__":
    # c = Coder("ctfs2")
    queriesFullStack = [
        """
        I want a real-time chat application where two people can talk to each other through the browser in a livechat-like environment. 
        Each of the users should have a name and the app should store the history of the conversation. 
        You should also allow for emoji use by having an emoji selector in input box. 
        Each message in the message timeline should be accompanied by a timestamp of the message and who sent it. 
        Messages most recently sent should be at the bottom of the message history.
        """,
        """
        build a responsive website and use gscp for animations and use pinning like technology 
        from gscp for designing and react tosttify for any notification
        """,
        """
        build a full stack chat application using 
        socket.io and authorisation using JWT Token and cookies and use SQL based database
        """,
        """
        build a real time video calling full stack app using webRTC
        """
    ]
    context = ""
    # c.code(queriesFullStack[2], context)

    # c = Coder("ct5oai")
    # queryOpenAI = """
    # Build a custom chatbot using OpenAI API that can act as my coding assistant and help me write code snippets for different tasks.
    # It should preserve history of the conversation and shut down once the task is complete.
    # """
    # openai_doc = ""
    # with open("./functions/openai.txt","r") as f:
    #     openai_doc = f.read()

    # c.code(queryOpenAI, openai_doc)

    """
    API example
    """
    c = Coder("ct4oaiapi")
    customdoc = """
    Method: GET
    URL: /api/customers
    Description: Get a list of all customer names

    Method: GET
    URL: /api/customer/{name}
    Description: Get a specific customer's details including Name, Username, Password and Phone Number in JSON format

    Method: POST
    URL: /api/customer/{name}/{password}
    Description: Add a new customer to the database with the given name and password

    Method: GET
    URL: /api/customer/{name}/login/{password}
    Description: Check if the customer with the given name and password exists in the database
    """
    query = f"""
    I want to build a chatbot application for my organisation.
    I want the chatbot to use the OpenAI API to generate responses to user queries.
    You will have access to a custom API documentation that you can use provide the following functionalities:
        - User Signup
        - User Login
    After verification, a user should be able to interact with the chatbot and get responses to their queries.
    """
    openai_doc = ""
    with open("./functions/openai.txt","r") as f:
        openai_doc = f.read()
    context = openai_doc + f"Custom API Documentation: {customdoc}"

    
    c.code(query, context)