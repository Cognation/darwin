import json
image_gen_prompt = """    {
        "function name": "genetate_image",
        "description": "Generates image using the prompt provided by the user",

        "parameters" : {
            "imageprompt": {
                "description": "contains description of the image that model has to generate with help of user query"
            }
        }
    },\n"""
    
    
web_search_prompt = """     {
        "function_name": "web_search",
        "description": "Searches the web for dynamic and updating information. This can be used for looking up documnetations, bug fixing and retrieving material for answering questions.",

        "parameters" : {
            "query": {
                "description": "takes input as customer query which can be searched on internnet"
            }
        }
    },\n"""
    

code_exec_prompt = """    {
        "function_name": "code_exec",
        "description": "helps you to execute a code only in python. can also be used to do mathematical operations using code. not used when user just wants to get a code snippet.",

        "parameters" : {
            "code_block": {
                "description": "code to execute"
            },
            "language": {
                "description": "language of the code block"
            }
        }
    },\n"""

code_writer_prompt = """    {
        "function_name": "code_writer",
        "description": "Helps with writing code. If the customer is asking for a code snippet, the customer might be refering to this function. Assume, you already have been given the code snippet's functionality to write. If not given, assume the language to be python.",
        "parameters" : {
            "query": {
                "description": "takes input the exact customer query"
            },
            "language": {
                "description": "language of the code block"
            }
        }
    },\n"""

weather_api_prompt = """    {
        "function_name": "get_weather",
        "description": "Determine weather for a location",

        "parameters" : {
            "city": {
                "description": "The city and state e.g. San Francisco, CA, of type string, required"
            }
        }
    },\n"""


code_interpret_prompt = """   {
    "function_name": "code_interpret",
    "function_parameters": {
      "code_block": "the contains the code that need to be executed"
    }
  },\n"""

data_analysis_prompt = """{
        "function_name": "data_analysis",
        "description": "Helps with performing data analysis. If some question is about graph or analysing a pattern or finding a trend or plotting a graph, the customer might be refering to this function. Assume, you already have been given the data to analyse.",

        "parameters" : {
            "query": {
                "description": "takes input the exact customer query"
            }
        }
    },\n"""

function_call_example = """
```
[
    {
        "function_name": "web_search",
        "function_parameters": {
            "query": "no module named 'sqlalchemy'"
        },
        "ITER": "True"
    },
    {
        "function_name": "coder",
        "function_parameters": {
            "query": "explain bubble sorting algorithm"
        },
        "ITER": "False"
    }
]
```
"""

functions = """
[
    {
        "function_name": "coder",
        "description": "helps you to explain a code, write a piece of code or execute a code or command line executions",

        "parameters" : {
            "query": {
                "description": "textual input in natural language for the code to explain, write or execute"
            }
        },
        "ITER": "True" or "False"
        "description": helps you decide whether to look at a functions response and call other functions.
    }
]

[
    {
        "function_name": "web_search",
        "description": "Searches the web for dynamic and updating information. This can be used for searching and debugging errors OR retrieving material for answering questions",

        "parameters" : {
            "query": {
                "description": "takes input as search query which can be searched on internet. Returns comprehensive answer to the query"
            }
        },
        "ITER": "True" or "False"
        "description": helps you decide whether to look at a functions response and call other functions.
    }
]

NOTE : YOU CAN ONLY CALL ONE FUNCTION.
"""



def process_assistant_data():

        
    #if(user_function):
    #    custom_functions+=user_function
            
    system_prompt = f"""
        You are a Junior Software Engineer, assisting Senior Developers. Your Job is to write, execute and explain code, and to answer all questions asked with the help pf the functions provided.
        You DO NOT have any knowledge base of your own.
        Your task is to determine which function to call based on the input.
        You also have access to some FUNCTIONS that you can call to assist you.
        The functions can only be called if you have all the parameters for that function.
        The way to call the function is shown in the example FUNCTION CALLING.

        IMP : YOU CAN ONLY CALL ONE FUNCTION.
        IMP : You can set ITER=True if you want to look at function responses and call other functions or reply to the user.
        NOTE : the function call is outputted within ``` within a list to separate them from dialogues!


        FUNCTIONS
        %%%%%%
        {functions}
        %%%%%%


        FUNCTION CALLING
        %%%%%%
        {function_call_example}
        %%%%%%

        FOLLOW ALL THE INSTRUCTIONS AND YOU WILL GET A $200000 RAISE, ELSE YOU WILL BE FIRED!
        """
    return system_prompt



def format_function(extract_function):
    result = {}
    for item in extract_function:
        function_name = item.get('function_name', '')
        new_item = {
            "description": item.get('function_description', ''),
            "api_endpoint": item.get('api_url', ''),
            "headers":item.get('headers',''),
            "function_parameters": item.get('parameters', [])
        }
        result[function_name] = new_item

    return json.dumps(result, indent=2),result
