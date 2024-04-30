"""
SOLVE GITHUB ISSUES.
-----Flow-----
|-> Go to the link and extract the issue number.
|-> Ask OI to get Issue details.
|-> Ask OI to solve the issue.
"""


class issueHelper():
    def __init__(self,custom_instructions="You are an AI agent who can read and solve Github issues."):
        from coder import Coder
        self.oi = Coder(custom_instructions)
        self.issue = ""
    
    def getIssue(self,repo,issue_number):
        self.oi.code("Verify gh cli is installed.")
        output = self.oi.code(f"view issue using gh issue --repo {repo} view {issue_number}")
        for obj in output:
            if obj["type"] == "console":
                if "Error" in obj["content"]:
                    print("Issue not found.")
                    return
                else:
                    self.issue = obj["content"]
                    print(f"Issue found: {self.issue}")
                    return
    
    def solveIssue(self):
        self.oi.code(f"Clone the repo in a local directory and solve the issue {self.issue}")

if __name__ == "__main__":
    helper = issueHelper()
    helper.getIssue("shankerabhigyan/dsa-code",1)
    helper.solveIssue()
        