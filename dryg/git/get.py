'''

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

