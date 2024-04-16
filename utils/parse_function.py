import json
import re

def extract_function_names(text):
    # Find JSON content within the text using regular expressions
    json_pattern = r'```(?:json)?(.*?)```'
    matches = re.findall(json_pattern, text, re.DOTALL)

    function_names = []

    for match in matches:
        try:
            # Parse the JSON content
            json_data = json.loads(match)
            # Iterate through the list of functions and extract the names
            for item in json_data:
                function_name = item.get('function_name')
                if function_name:
                    function_names.append(function_name)
        except json.JSONDecodeError as e:
            print(f"Error decoding function name JSON: {e}")

    return function_names


def extract_function_parameters(text):
    # Find JSON content within the text using regular expressions
    json_pattern = r'```(?:json)?(.*?)```'
    matches = re.findall(json_pattern, text, re.DOTALL)

    parameter_list = []

    for match in matches:
        try:
            # Parse the JSON content
            json_data = json.loads(match)
            # Iterate through the list of functions and extract the parameters
            for item in json_data:
                function_parameters = item.get('function_parameters')
                params = dict()
                if function_parameters:
                    for key, value in function_parameters.items():
                      params[key] = value
                    parameter_list.append(params)
        except json.JSONDecodeError as e:
            print(f"Error decoding function parameters JSON: {e}")

    return parameter_list

def extract_iter(text):
    # Find JSON content within the text using regular expressions
    json_pattern = r'```(?:json)?(.*?)```'
    matches = re.findall(json_pattern, text, re.DOTALL)

    ITER = False

    for match in matches:
        try:
            # Parse the JSON content
            json_data = json.loads(match)
            # Iterate through the list of functions and extract the parameters
            for item in json_data:
                if "ITER" in item:  # Check if ITER key exists
                    iter_value = item["ITER"]
                    if isinstance(iter_value, bool):
                        ITER = iter_value
                    elif isinstance(iter_value, str) and iter_value.lower() == "false":
                        ITER = False
                    elif isinstance(iter_value, str) and iter_value.lower() == "true":
                        ITER = True
                    else:
                        print("ITER value is not boolean.")
                else:
                    print("ITER key is missing in the JSON data.")
        except json.JSONDecodeError as e:
            print(f"Error decoding ITER JSON: {e}")

    return ITER

if __name__ == "__main__":
    # Example usage:
    text_output = """
     ```
    [
        {
            "function_name": "coder",
            "function_parameters": {
                "query": "clone https://github.com/shankerabhigyan/dsa-code.git in './dsa-code'" 
            }, 
            "ITER": "False"
        }
    ]
    ```
    """

    function_names = extract_function_names(text_output)
    print(function_names)
    function_parameters = extract_function_parameters(text_output)
    print(function_parameters)
    iter = extract_iter(text_output)
    print(iter,type(iter))