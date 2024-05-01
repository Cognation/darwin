import subprocess
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class issueHelper():
    def __init__(self,project_name):
        self.project_name = project_name
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        prompt = "You are a helpful AI assistant who analyses Github Issue texts and generates a summary of the issue and creates a list of files to be analysed or edited."
        self.message = [
            {"role": "system", "content": prompt}
        ]
        self.openai = openai.OpenAI(api_key=self.openai_api_key)

    def getIssue(self,repo,issue_number):
        # gh issue --repo {repo} view {issue_number}
        self.issue = subprocess.run(["gh", "issue", "--repo", repo, "view", str(issue_number)],capture_output=True)
        self.issue = self.issue.stdout.decode("utf-8")        
    
    def getIssueSummary(self,repo,issue_number):
        self.getIssue(repo,issue_number)
        self.message.append({"role":"user","content":self.issue})
        self.issue_summary = self.openai.chat.completions.create(
            model = "gpt-4-turbo",
            messages = self.message,
            temperature=0.5
            )
        return self.issue_summary.choices[0].message.content
    

if __name__ == "__main__":
    helper = issueHelper("first")
    response = helper.getIssueSummary("shankerabhigyan/dsa-code","1")
    print(response)