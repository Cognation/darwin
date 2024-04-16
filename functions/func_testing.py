from coder import *
import datetime

# query = input("Enter your query: ")
# OIquery(query)

interpreter.system_message = """
    Run shell commands with -y so the user doesn't have to confirm them.
    """

def write_logs(response):
    with open("OIlogs.txt", "a") as f:
        f.write(str(datetime.datetime.now()) + "\n")
        for message in response:
            # dict to string
            message = str(message)
            f.write(message+"\n")
        f.write("\n\n\n")

history = []
while True:
    message = input("Write a message: ")
    response = coder(message)
    print(response)
    history = history + response
    write_logs(response)
