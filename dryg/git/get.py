'''
There are many ways to go about handling github rest apis. What I'm going for is a simplecway to get the data I need without 
making too many calls to the api. The idea is:
* To get all repos for the user during the initial setup and create a table with all the granular details of the repo.
* Other ooerations such as selecting repos based on certain criteria, getting issues, etc. can be done on the table without additional need to call the api.
* The table can be updated periodically to keep it in sync with users github account.
'''
from github import Github
from github.PaginatedList import PaginatedList
import pyarrow.compute as pc

from dryg.db import open_table
from dryg.settings import WEIGHTS_URI

GH = Github()

def get_all_repos()-> PaginatedList:
    """
    Get all repos for the user

    Returns:
        PaginatedList: List of repos
    """
    user = GH.get_user("AyushExel")
    orgs = user.get_orgs()
    user_repos = list(user.get_repos())
    org_repos = [org_repo for org in orgs for org_repo in org.get_repos()]
    all_repos = user_repos + org_repos

    return all_repos

def get_repo_names_ending_with(name: str):
    """
    Get a repo by name
    
    Args:
        name (str): Name of the repo
    """
    repos_table =  open_table("repos")
    if not repos_table:
        raise ValueError("Repos table not found. Initialize the app by running `dryg init`")
    repos_pa = repos_table.to_arrow()
    result = pc.filter(repos_pa, pc.ends_with(repos_pa["full_name"], name, ignore_case=True))
    return result["full_name"].to_pylist()

def get_issues(repo, **kwargs):
    """
    Get issues for a repo

    Args:
        repo (str): Name of the repo
        **kwargs: Keyword arguments to be passed to the github api

    Returns:
        PaginatedList: List of issues
    """
    repo = GH.get_repo(repo)
    issues = repo.get_issues(state="all", **kwargs)
    return issues

def get_issue_comments(repo, issue_number):
    """
    Get comments for an issue

    Args:
        repo (str): Name of the repo
        issue_number (int): Issue number

    Returns:
        PaginatedList: List of comments
    """
    repo = GH.get_repo(repo)
    issue = repo.get_issue(issue_number)
    comments = issue.get_comments()
    return comments
