from .dalle import imagegenerator
from .web_api import web_search
from .weather_api import get_weather
from .code_exec import code_exec
from .data_analysis import data_analysis
from .code_writer import code_writer
from .code_interpret import code_interpret
from .coder import coder
from .web_api import web_search
function_dict = {
    "generate_image" : imagegenerator,
    "web_search" : web_search, 
    "code_exec" : code_exec,
    "get_weather":get_weather,
    "data_analysis":data_analysis,
    "code_writer":code_writer,
    "code_interpret":code_interpret,
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
