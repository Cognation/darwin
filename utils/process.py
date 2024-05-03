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
            "statement": "Can you tell me more about the issue number 1167 from the repo gpt-neox from EleutherAI?"
        }
    }
]
```
"""

functions = """
function_name : web_search
description : Searches the web for dynamic and updating information. This can be used for searching and debugging errors OR retrieving relevant code documentation for answering web queries.

function_name : coder
description : helps you to explain a code, write a piece of code or execute a code or command line executions

function_name : summary_text
description : Used to send message, concluding your work to the senior devs if you are satisfied with the function response

function_name : getIssueSummary
description : Get the summary of the issue from the github repository
"""



def process_assistant_data(original_query,StateOfMind):

        
    #if(user_function):
    #    custom_functions+=user_function
            
    system_prompt = f"""
    You have the important role of assisting the user with their queries using various functions available.

    FUNCTIONS:
    {functions}
    
    EXAMPLES of function call:
    {function_call_example}

    Remember:
    - You can only call one function at a time.
    - After receiving a satisfactory "State Of Mind" response, proceed to call the "summary_text" function.
    - Avoid redundant calls by only invoking functions when necessary.
    - Keep all functions within ``` ```
    - Follow the function call exactly as shown in the example above.

    Original Query:
    {original_query}

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
