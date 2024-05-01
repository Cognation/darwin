"""
SOLVE GITHUB ISSUES.
-----Flow-----
|-> Go to the link and extract the issue number.
|-> Ask OI to get Issue details.
|-> Parse relevant file data and return.
"""


class issueHelper():
    def __init__(self,project_name,custom_instructions="You are an AI agent who has to study and return all relevant information on a specific Github issue asked."):
        from coder import Coder
        self.oi = Coder(project_name,custom_instructions)
        self.issue = ""
    
    def getIssue(self,repo,issue_number):
        self.oi.code("Verify gh cli is installed.")
        self.repo = repo
        self.issue_number = issue_number
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
    
    def getIssueData(self):
        query = f"""
            1. Clone the repo {self.repo} in {self.oi.path} under original repo name folder. 
            2. Create a new file named 'issue_data.txt' in {self.oi.path} directory. In this file write the issue {self.issue} using with..open() function.
            3. Analyse the files in the cloned repository and write a list of all files that are relevant to the issue {self.issue} to 'issue_data.txt'.
            """
        # create a list of all instructions
        query_list = query.split("\n")
        self.oi.code(query_list[0])
        self.oi.code(query_list[1])
        self.oi.code(query_list[2])
        return 
    

if __name__ == "__main__":
    helper = issueHelper("first")
    helper.getIssue("shankerabhigyan/dsa-code",1)
    helper.getIssueData()
        