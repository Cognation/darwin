from .web_api import web_search
from .coder import coder
function_dict = {
    #"generate_image" : imagegenerator,
    #"get_weather":get_weather,
   # "data_analysis":data_analysis,
    "coder":coder,
    "web_search":web_search
}

def execute_functionsl(function_names, function_parameters):
    result = {}
    for name, parameters in zip(function_names, function_parameters):
        if name in function_dict and function_dict[name] is not None:
            try:
                result[name] = function_dict[name](**parameters)
            except Exception as e:
                result[name] = f"Error executing function '{name}': {str(e)}"
        else:
            result[name] = f"Function '{name}' not found or not implemented."

    return result
