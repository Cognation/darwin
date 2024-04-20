import os
import json
from uuid import uuid4
from typing import List
import ast
from openai import OpenAI
from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
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

# Initialize FastAPI app
app = FastAPI()

global_state = {
    "OI_chat": [],
    "OI_history": [],
    "project_id": ""
}

async def update_global_state(key, val):
    global global_state
    global_state[key] = val

async def get_global_state(key):
    global global_state
    return global_state[key]

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

async def update_db(project_id, key, val):
    project = db.get(project_id)
    project[key] = val
    db.set(project_id, project)

# Constants
MODEL_NAME =  "gpt-4-0125-preview"  # config('MODEL_NAME')
MAX_TOKENS = 150
TEMPERATURE = 0.7

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


@app.post("/create_project") # creates a new project and updates the global state with the project data
async def create_project(request: Request):
    data = await request.form()
    project_name = data.get("project_name")
    project_id = str(uuid4()) 
    db.set(project_id, {"project_name": project_name, "OI_history": [], "OI_chat": []})
    await update_global_state("project_id", project_id)
    await update_global_state("OI_chat", [])
    await update_global_state("OI_history", [])
    return {"project_id": project_id, "project_name": project_name}

@app.post("/get_project_data") # updates the global state with the project data
async def get_project(request: Request):
    data = await request.form()
    project_id = data.get("project_id")
    all = db.getall()
    dict = {}
    for key in all:
        if key == project_id:
            project_name = db.get(key)["project_name"]
            oichat = db.get(key)["OI_chat"]
            oihistory = db.get(key)["OI_history"]
            dict = {"project_id": project_id, "project_name": project_name, "OI_chat": oichat, "OI_history": oihistory}
            await update_global_state("project_id", project_id)
            await update_global_state("OI_chat", oichat)
            await update_global_state("OI_history", oihistory)
    return dict

    

@app.delete("/delete_project") # deletes the project
async def delete_project(request: Request):
    data = await request.form()
    project_id = data.get("project_id")
    if(project_id == 'all'):
        for key in db.getall():
            db.rem(key)
        return {"message": "All projects deleted successfully"}
    for key in db.getall():
        if key == project_id:
            db.rem(key)
            return {"message": "Project deleted successfully"}
    return {"message": "Project not found"}
    
@app.get("/get_project_ids") # returns key value pairs of id and project name
async def get_projects():
    list = []
    for key in db.getall():
        project_id = key
        project_name = db.get(key)["project_name"]
        list.append({"project_id": project_id, "project_name": project_name})
    return list

@app.post("/chat")

async def chat(request: Request,file: UploadFile = None,image: UploadFile = None):
    """
    FORM DATA FORMAT:
    {
        "unique_id": "user_id",
        "assistant_name": "assistant_name",
        "session_id": "session_id",
        "customer_message": "message",
    }
    """
    data = await request.form()
    project_id = data.get("project_id")
    customer_message = data.get("customer_message")
    # content = ""
    # secondary_knowledge = ""
    # save_path_da = f"user_data/{user_id}/{assistant_name}/data_analysis"
    # check if save_path_da exists else create it
    # if not os.path.exists(save_path_da):
    #    os.makedirs(save_path_da)
    

    # server_response = dict()
    server_response = ""
    await update_global_state("project_id", project_id)
    old_chat = await get_global_state("OI_chat")
    chat = old_chat + [{"User":customer_message}]
    # parse chat for openai prompt
    openai_chat = json.dumps(chat)
    await update_global_state("OI_chat",chat)
    while(True):
        res = await chatGPT(customer_message,openai_chat)
        result = res.get("result")
        print("Res.Iter: ",res.get("iter"))
        function_response = res.get("function_response")
        func = res.get("func")
        iter = bool(res.get("iter"))
        print("\n\niter",iter)
        if func:
            # chat = add_chat_log(func, function_response.get(func), chat)
            server_response = function_response.get(func)
            if(func=="coder"):
                for obj in server_response:
                    if obj["role"]=="assistant" and obj["type"]=="message":
                        old = await get_global_state("OI_chat")
                        old = old + [{"Assistant":obj["content"]}]
                        await update_global_state("OI_chat",old)     
                old = await get_global_state("OI_history")
                await update_global_state("OI_history",old+function_response.get(func))
            if(func=="web_search"):
                old = await get_global_state("OI_chat")
                old = old + [{"Assistant":server_response["message"]}]
                await update_global_state("OI_chat",old)
        else:
            # chat = add_chat_log("assitant",result,chat)
            server_response = result
            old = await get_global_state("OI_chat")
            old = old + [{"Assistant":server_response}]
            await update_global_state("OI_chat",old)
        print(chat)
        print("ITER: ",iter)
        if(not iter):
            break
    await update_db(project_id, "OI_chat", await get_global_state("OI_chat"))
    await update_db(project_id, "OI_history", await get_global_state("OI_history"))
    return server_response

def add_chat_log(agent, response, chat_log=""):
    return f"{chat_log}{agent}: {response}\n"

async def chatGPT(customer_message,chat):
    res ={
        "result":None,
        "function_response":None,
        "func":None,
        "iter":False
    }
    prompt = process_assistant_data()
    message = [
        {"role": "system", "content": prompt},
        {"role": "assistant", "content":chat},
        {"role": "user", "content": customer_message},
    ]
    print("\nMessage to GPT: \n", message)
    gpt_response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=message,
        temperature=TEMPERATURE,
    )
    print("\ngpt_response",gpt_response)
    result = gpt_response.choices[0].message.content
    print("\n\nResult: \n", result)

    functions = extract_function_names(result)
    res["result"] = result    
    res["iter"] = bool(extract_iter(result))

    # print("\nChat: \n", chat)    
    print("\nFunctions: \n", functions)
    
    function_response = dict()
    if functions:
        parameters = extract_function_parameters(result)
        for func, parameter in zip(functions, parameters):
            res["func"] = func
            print(func)
            print(parameter)
            try:
                if func in function_dict:
                    if func == "coder":
                        oichat = await get_global_state("OI_chat")
                        oihistory = await get_global_state("OI_history")
                        query = parameter['query']
                        coder_response = (coder(query, oichat, oihistory))
                        function_response.update({"coder":coder_response})
                    elif func == "web_search":
                        response = (web_search(parameter['query']))
                        function_response.update({"web_search":response})
                    else:
                        function_response.update(function_dict[func](**parameter))
            except Exception as e:
                print(f"Error calling the function {func} with parameters {parameter}: {e}")
    res["function_response"] = function_response
    return res

# start the server
if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    print(os.environ["OPENAI_API_KEY"])
    openai = OpenAI(api_key=openai_api_key)
    uvicorn.run(app, host="0.0.0.0", port=8080)
