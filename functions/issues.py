import subprocess
import openai
import os
import re
import json

class issueHelper():
    def __init__(self,project_name):
        self.project_name = project_name
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        prompt = "You are a helpful AI assistant who analyses Github Issue texts and generates a summary of the issue and creates a list of files to be analysed or edited."
        self.message = [
            {"role": "system", "content": prompt}
        ]
        self.openai = openai.OpenAI(api_key=self.openai_api_key)

    def parse_response(self, response):
        response = response.strip()
        return json.loads(response)

    def getIssue(self,statement):
        # gh issue --repo {repo} view {issue_number}
        prompt = """You are a helpful AI assistant, who can read and identify github repository and issue number from the user's statement or link,
        and return them parsed perectly as a clean JSON object.
        {
            "repo": "shankerabhigyan/dsa-code",
            "issue_number": "1"
        }
        """
        message = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": statement}
        ]
        response = self.openai.chat.completions.create(
            model = "gpt-4-turbo",
            messages = message,
            temperature=0.5
        )
        response = response.choices[0].message.content
        # print("Response : ",response)
        response_json = self.parse_response(response)
        # print("Response JSON : ",response_json)
        repo = response_json["repo"]
        issue_number = response_json["issue_number"]
        # print("Repo : ",repo)
        # print("Issue Number : ",issue_number)
        self.issue = subprocess.run(["gh", "issue", "--repo", repo, "view", str(issue_number)],capture_output=True)
        self.issue = self.issue.stdout.decode("utf-8")    
        # print("Issue : ",self.issue)    
    
    def getIssueSummary(self,statement): # make param a statement in natural language
        self.getIssue(statement)
        # print("Issue : ",self.issue)
        self.message.append({"role":"user","content":self.issue})
        self.issue_summary = self.openai.chat.completions.create(
            model = "gpt-4-turbo",
            messages = self.message,
            temperature=0.5
            )
        return self.issue_summary.choices[0].message.content
    

if __name__ == "__main__":
    helper = issueHelper("testing10")
    # response = helper.getIssueSummary("Whats the issue here https://github.com/shankerabhigyan/dsa-code/issues/1")
    #response = helper.getIssueSummary("Whats the issue here https://github.com/EleutherAI/gpt-neox/issues/1204 can you help?")
    
    response = helper.getIssueSummary("Can you tell me more about the issue number 86 from the repo pickledb from patx?")
    #helper.getIssue("tell me about the issue https://github.com/EleutherAI/gpt-neox/issues/1204")
    print(response)