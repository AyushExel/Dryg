'''
There are many ways to go about handling github rest apis. What I'm going for is a simplecway to get the data I need without 
making too many calls to the api. The idea is:
* To get all repos for the user during the initial setup and create a table with all the granular details of the repo.
* Other ooerations such as selecting repos based on certain criteria, getting issues, etc. can be done on the table without additional need to call the api.
* The table can be updated periodically to keep it in sync with users github account.
'''

import github
from github import Github

GH = Github("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")

def get_all_repos():
    user = GH.get_user()
    orgs = user.get_orgs()

    user_repos = list(user.get_repos())
    org_repos = [org_repo for org in orgs for org_repo in org.get_repos()]
    all_repos = user_repos + org_repos

    return all_repos

def get_repo_by_name(name: str):
    repo =  GH.get_repo(name)
    import pdb; pdb.set_trace()

def get_issues(repo, **kwargs):
    return list(repo.get_issues(**kwargs))

