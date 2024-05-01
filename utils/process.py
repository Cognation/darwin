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
            "query": "what is bubble sort in python?"
        }
    }
]
```

```
[

    {
        "function_name": "coder",
        "function_parameters": {
            "query": "write a python code for bubble sort algorithm."
        }
    }
]
```

```
[
    {
        "function_name": "summary_text",
        "function_parameters": {
            "message": "The bubble sort algorithm is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. I have written relevant code for the same..."
        }
    }
]
```

```
[
    {
        "function_name": "getIssueSummary",
        "function_parameters": {
            "repo": "shankerabhigyan/dsa-code",
            "issue_number": "24"
        }
    }
]
```
"""

functions = """
[
    {
        "function_name": "web_search",
        "description": "Searches the web for dynamic and updating information. This can be used for searching and debugging errors OR retrieving relevant code documentation for answering web queries.",

        "parameters" : {
            "query": {
                "description": "takes input as search query which can be searched on internet. Returns comprehensive answer to the query"
            }
        }
    },

    {
        "function_name": "coder",
        "description": "helps you to explain a code, write a piece of code or execute a code or command line executions",

        "parameters" : {
            "query": {
                "description": "textual input in natural language for the code to explain, write or execute"
            }
        }
    },


    {
        "function_name": "summary_text",
        "description": "Used to send message, concluding your work to the senior devs if you are satisfied with the function response",
        "parameters" : {
            "message": {
                "description": "message to send to the user. Should contain a summary of the function response."
            }
        }
    },

    {
        "function_name": "getIssueSummary",
        "description": "Get the summary of the issue from the github repository",
        "parameters" : {
            "repo": {
                "description": "The repository name from which the issue is to be fetched eg. shankerabhigyan/dsa-code"
            },
            "issue_number": {
                "description": "The issue number to be fetched eg. 24"
            }
        }
    }
]
```
"""



def process_assistant_data(StateOfMind):

        
    #if(user_function):
    #    custom_functions+=user_function
            
    system_prompt = f"""
        You are an AI Software Engineer Intern, Your job is to assist the user in their queries.
        You have a simple task of assisting the user in their queries. You can help the user with the following functions:
        {functions}
        Based upon your State Of Mind, you will decide which function to call.
        You can only call one function at a time, based on which your StateOfMind will be updated, reflecting the summary result of the function call.
        When you are satisfied with the StateOfMind, you can call the summary_text function to send a message to the user and conclude your work.

        FUNCTION CALL EXAMPLES:
        {function_call_example}

        Keep all functions within ``` ```.
        Follow the above instructions precisely to get a bonus. Else you will be penalized.

        STATE OF MIND:
        {StateOfMind}
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
