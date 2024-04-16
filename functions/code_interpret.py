# import os
# import openai
# from dotenv import load_dotenv
# env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(env_path)
# openAI_key = os.getenv("OPENAI_API_KEY")

# def code_interpret(code_block):
#     # use gpt 4 to explain the code
#     openai.api_key = openAI_key
#     prompt = "Explain the following code: \n" + code_block
#     response = openai.Completion.create(
#       engine="gpt-4",
#       prompt= prompt,
#       max_tokens=200
#     )
#     return {"message": response.choices[0].text}