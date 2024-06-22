import os
import json
from uuid import uuid4
from typing import List
import ast
from openai import OpenAI
from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import fastapi
from decouple import config
from gridfs import GridFS
from PIL import Image
import io
import mimetypes
import pandas as pd
import asyncio
from utils.process import *
from utils.fileparse import *
from utils.parse_function import extract_function_names, extract_function_parameters, extract_iter
from functions.coder import *
from functions.web_api import *
from functions.call_function import function_dict
from functions.extract_web_links import extract_links, scrape_pdf
import copy
import traceback


# Initialize FastAPI app
app = FastAPI()
global history
global web_search_response
global StateOfMind
web_search_response = ""
history = ""
StateOfMind = ""
cc = 0
iter = 0
prevcoder = False

# Enable CORS for all routes
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import pickledb
db = pickledb.load('./data/data.db', True) 

def update_db(project_name, val):
    project = db.get(project_name)
    project.append(val)
    db.dump()
    
def get_db(project_name):
    project = db.get(project_name)
    return copy.deepcopy(project)

from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("MODEL")
MAX_TOKENS = 10000
TEMPERATURE = 0

def convert_bytes_to_original_format(file_bytes, mime_type, save_path):
    if mime_type.startswith('text'):
        # Save text file
        with open(save_path, 'w', encoding='utf-8') as text_file:
            text_file.write(file_bytes.decode('utf-8'))
    elif mime_type.startswith('image'):
        # Save image file
        img = Image.open(io.BytesIO(file_bytes))
        img.save(save_path)
    elif mime_type == 'application/json':
        # Save JSON file
        with open(save_path, 'w', encoding='utf-8') as json_file:
            json.dump(json.loads(file_bytes.decode('utf-8')), json_file, indent=2)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        # Save Excel file
        df = pd.read_excel(io.BytesIO(file_bytes))
        df.to_excel(save_path, index=False)
    elif mime_type == 'application/pdf':
        # Save PDF file
        # Example: pdf_to_text_and_save(file_bytes, save_path)
        pass
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Save DOCX file
        doc = Document(io.BytesIO(file_bytes))
        doc.save(save_path)
    else:
        # Handle other types or raise an exception for unknown types
        raise ValueError(f"Unsupported MIME type: {mime_type}")



def store_file_in_mongodb(file_path, collection_name):
    fs = GridFS(db, collection=collection_name)
    with open(file_path, 'rb') as file:
        # Determine file type using mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        metadata = {'mime_type': mime_type}

        file_id = fs.put(file, filename=os.path.basename(file_path), metadata=metadata)

    return file_id

def retrieve_file_from_mongodb(file_id, collection_name):
    fs = GridFS(db, collection=collection_name)
    file_data = fs.get(file_id)

    # Retrieve metadata
    metadata = file_data.metadata
    mime_type = metadata.get('mime_type', 'application/octet-stream')

    return file_data.read(), mime_type


def get_folder_structure(dir_path,parent=""):
    is_directory = os.path.isdir(dir_path)
    name = os.path.basename(dir_path)
    relative_path = os.path.relpath(dir_path, os.path.dirname(dir_path))

    directory_object = {
        'parent': os.path.dirname(dir_path),
        'path': relative_path,
        'name': name,
        'type': 'directory' if is_directory else 'file',
    }

    if is_directory:
        children = []
        for child in os.listdir(dir_path):
            child_path = os.path.join(dir_path, child)
            children.append(get_folder_structure(child_path,parent=dir_path))
        directory_object['children'] = children

    return directory_object


@app.post("/serve_file")
async def serve_file(request: Request):
    data = await request.form()
    filePath = data["path"]
    # serve file using fastapi FileResponse
    pwd = os.path.join(os.getcwd(), 'data')
    path = os.path.join(pwd, filePath)
    return fastapi.responses.FileResponse(path)

@app.post("/folder_structure")
async def folder_structure(request:Request):
    data = await request.form()
    root_dir = data["root_dir"]
    structure = get_folder_structure(root_dir)
    return structure

@app.get("/get_file")
async def get_file(request: Request):
    data = await request.form()
    path = data["path"]
    with open(path, "rb") as file:
        file_bytes = file.read()
    return file_bytes

@app.post("/create_project") # creates a new project and updates the global state with the project data
async def create_project(request: Request):
    data = await request.form()
    project_name = data.get("project_name")
    # check if project already exists
    for key in db.getall():
        if key == project_name:
            return {"message": "Project already exists"}
    db.set(project_name,[])
    return {"project_name": project_name}

@app.post("/get_project_data") # updates the global state with the project data
async def get_project(request: Request):
    data = await request.form()
    project_name = data.get("project_name")
    project = db.get(project_name)
    print(project)
    return project

@app.delete("/delete_project") # deletes the project
async def delete_project(request: Request):
    data = await request.form()
    project_name = data.get("project_name")
    for key in db.getall():
        if key == project_name:
            db.rem(key)
            return {"message": "Project deleted successfully"}
    return {"message": "Project not found"}

# get    
@app.get("/get_project_names") # returns key value pairs of id and project name
async def get_projects():
    list = []
    for key in db.getall():
        project_name = key
        list.append(project_name) 
    return list

### HANDLING OUTPUT STREAMING
pyth_messages = []
@app.post("/out")
async def catch(request: Request):
    data = await request.form()
    agent = data.get("agent")
    text = data.get("text")
    pyth_messages.append({"agent":agent, "text":text})
    return {"status": "OK"}

### HANDLING STREAM
# get
@app.get('/stream')
async def stream_data():
    async def generate():
        while True:
            if pyth_messages:
                temp = pyth_messages.copy()
                pyth_messages.clear()
                for message in temp:
                    yield json.dumps(message) + "\n"
            await asyncio.sleep(.5)
    return StreamingResponse(generate(), media_type='text/event-stream')

### HANDLING INPUT STREAMING
input_messages  = {}
prompt_id = ""
# get
@app.get("/in")
async def catch_request(request: Request):
    global input_messages
    data = await request.form()
    message = data.get("prompt")
    prompt_id = str(uuid4())
    pyth_messages.append({"in":message, "prompt_id":prompt_id})
    print(f"""
          curl --location 'http://localhost:8080/in/response' --form 'prompt_id="{prompt_id}"' --form 'response=""'
          """)
    while True:
        if prompt_id in input_messages:
            response = input_messages[prompt_id]
            del input_messages[prompt_id]
            return {"input": response}
        await asyncio.sleep(.5)
# get
@app.get("/request_project_name")
async def get_project_name(request: Request):
    global project_name
    print("Sending project name:", project_name)
    return {"project_name": project_name}
# get
@app.get("/request_user_query")
async def get_user_query(request: Request):
    global StateOfMind
    print("Sending user query:", StateOfMind)
    return {"user_query": StateOfMind}

@app.post("/in/response")
async def catch_response(request: Request):
    global input_messages
    data = await request.form()
    prompt_id = data.get("prompt_id")
    response = data.get("response")
    input_messages[prompt_id] = response
    print(input_messages)
    return {"status": "OK"}


    

@app.post("/chat")
async def chat(request: Request,file: UploadFile = None,image: UploadFile = None):
    """
    FORM DATA FORMAT:
    {
        "project_name": "project_name",
        "customer_message": "message"
    }
    """
    data = await request.form()
    global project_name
    project_name = data.get("project_name")
    customer_message = data.get("customer_message")
    global StateOfMind 
    StateOfMind = customer_message
    original_query = customer_message
    global history
    global prevcoder
    prevcoder = False
    history = get_db(project_name) if project_name in db.getall() else []
    history.append({"user_query":original_query})
    update_db(project_name,{"user_query":original_query})
    return StreamingResponse(chatGPT(project_name,original_query))


import subprocess
from core.cli.main import run_pythagora

def get_project_id(project_name):
    db_path = os.path.join(os.getcwd(), 'data', 'state.db')
    db = pickledb.load(db_path, True)
    project_id = db.get(project_name)
    return project_id

def chatGPT(project_name,original_query):
    global history
    global web_search_response
    global StateOfMind
    global cc
    global iter
    cont = False
    prevcall = None
    while(True):
        iter+=1
        prompt = process_assistant_data(original_query,StateOfMind,prevcall)
        history = get_db(project_name)
        history_string = ""
        for obj in history:
            history_string += f"User: {obj['user_query']}\n" if "user_query" in obj else ""
            history_string += f"AI_Coder_Message: {obj['message']}\n" if "message" in obj else ""
            history_string += f"AI_Coder_Code: {obj['code']}\n" if "code" in obj else ""
            history_string += f"AI_Coder_Output: {obj['console']}\n" if "console" in obj else ""
            history_string += f"Web_search: {obj['web_search']}\n" if "web_search" in obj else ""
        print("history" ,history_string)
        # truncate history string to turboo context length?
        message = [
            {"role": "system", "content": history_string},
            {"role": "user", "content": prompt}
        ]
        print("\nMessage to GPT: \n", prompt)
        gpt_response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=message,
            temperature=TEMPERATURE,
        )
        print("\ngpt_response",gpt_response)
        result = gpt_response.choices[0].message.content.strip()
        print("\n\nResult: \n", result)

        functions = extract_function_names(result)
        print("\nFunctions: \n", functions)
        
        if functions:
            parameters = extract_function_parameters(result)
            func = functions[0]
            parameter = parameters[0]
            print(func)
            print(parameter)
            try:
                if func == "coder":
                    if cont:
                        run_pythagora(get_project_id(project_name))
                    succ = run_pythagora()
                    if succ==-1:
                        cont = True
                        # get relevant error information
                    break
                    
                elif func == "web_search":
                    
                    response = web_search(parameter['query'])
                    out = json.dumps({"web_search":str(response)})
                    yield out.encode("utf-8") + b"\n"
                    update_db(project_name,{"web_search":str(response)})
                    web_search_response = response
                    StateOfMind = "Browsed the web and retrieved relevant information. Call the coder function or return to user."
                    prevcall = "web_search"
                    
                elif func == "summary_text":
                    prevcall = "summary_text"
                    response = (parameter['message'])
                    # check for ` in response and remove it
                    response = response.replace("`","")
                    out = json.dumps({"summary_text":response})
                    yield out.encode("utf-8") + b"\n"
                    update_db(project_name,{"summary_text":response})
                    yield b''
                    cc = 0
                    iter = 0
                    break

                elif func == "getIssueSummary":
                    from functions.issues import issueHelper
                    prevcoder = False
                    statement = parameter['statement']
                    issue_helper = issueHelper(project_name)
                    issue_summary = issue_helper.getIssueSummary(statement)
                    StateOfMind = "The issue details have been extracted as follows : \n" + issue_summary + "\n\n NOTE : Call the summary_text function to answer user's query or Coder function to solve the issue."
                    out = json.dumps({"getIssueSummary":issue_summary})
                    yield out.encode("utf-8") + b"\n"
                    update_db(project_name,{"getIssueSummary":issue_summary})
            except Exception as e:  
                print(f"Error calling the function {func} with parameters {parameter}: {e}")
                traceback.print_exc()
        else:
            pass
        
    

# start the server
if __name__ == "__main__":
    import uvicorn
    openai_api_key = os.getenv("OPENAI_API_KEY")
    print("OpenAI API Key:", openai_api_key)
    openai = OpenAI(api_key=openai_api_key)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)

    global project_name
    project_name = ""

    uvicorn.run(app, host="0.0.0.0", port=parser.parse_args().port)
