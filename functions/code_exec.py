import requests
from interpreter import interpreter

def code_exec(query):
    code_block = query['code_block']
    language = query['language']

    out = interpreter.computer.run(language, code_block)
    print(out)


# sampleQuery = {
#    "code_block": "total_expense = 16347 + 183\naverage_expense_per_night = total_expense / 9\nprint(total_expense, average_expense_per_night)",
#    "language": "python"
#}

# run(sampleQuery)