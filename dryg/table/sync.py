from dryg.git.get import get_all_repos, get_issues, get_repo_by_name

def create_repo_table():
    repos = get_all_repos()
    