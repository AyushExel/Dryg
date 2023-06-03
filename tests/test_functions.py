import github
from dryg.git.get import get_all_repos, get_issues, get_repo_by_name

'''
def test_get_repos():
    repos = get_all_repos()
    assert isinstance(repos, list), "Expected list of repos"

def test_get_issues():
    repos = get_all_repos()
    issues = get_issues(repos[0])
    assert isinstance(issues, list), "Expected list of issues"
'''

def test_get_repo_by_name():
    repo = get_repo_by_name("ultralytics")
    assert isinstance(repo, github.Repository.Repository), "Expected repo object"