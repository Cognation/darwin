from openai import OpenAI
import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)
openAI_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openAI_key)

def code_writer(query, language):
    # use gpt 4 to write the code
    prompt = "Write a code snippet in " + language + " to " + query
    message = [
        {"role": "system", "content": "You are a code writing AI. You can write code in any language. Return the code block within ```*``` Keep the code clean and void of any syntax errors. Do not mention language name within the snippet"},
        {"role": "user", "content": prompt},
        {"role": "system", "content": "The code snippet is as follows:"}
    ]
    gpt_response = client.chat.completions.create(
        model="gpt-4",
        messages=message,
        max_tokens=500,
        temperature=0.7,
    )
    result = gpt_response.choices[0]
    message =  result.message.content
    return {"message": message}
    