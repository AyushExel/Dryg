import lancedb
from github.PaginatedList import PaginatedList

from dryg.settings import REPO_SCHEMA, ISSUE_SCHEMA
from dryg.git.get import get_all_repos, get_issues
from dryg.table.create import create_repos_table, create_issues_table

CACHE = {} # This is a hack to avoid making too many calls to the api

def test_get_repos():
    repos = get_all_repos()
    assert isinstance(repos, PaginatedList), "Expected PaginatedList of repos"
    CACHE['repos'] = repos

def test_get_issues():
    repos = CACHE.get("repos") or get_all_repos()
    issues = get_issues(next(iter(repos)).full_name)
    assert isinstance(issues, PaginatedList), "Expected PaginatedList of issues"

'''
TODO: Fix this test
def test_get_repo_by_name():
    repo = get_repo_by_name("ultralytics")
    assert isinstance(repo, github.Repository.Repository), "Expected repo object"
'''

def test_create_repo_table():
    db = create_repos_table()
    assert isinstance(db, lancedb.LanceDBConnection), "Expected LanceDBConnection"
    repos = db.open_table('repos')
    assert repos.schema.names == REPO_SCHEMA, "Expected schema to match REPO_SCHEMA"

def test_create_issues_table():
    db = create_issues_table("ultralytics")
    assert isinstance(db, lancedb.LanceDBConnection), "Expected LanceDBConnection"
    issues = db.open_table('ultralytics')
    assert issues.schema.names == ISSUE_SCHEMA, "Expected schema to match REPO_SCHEMA"
    import pdb; pdb.set_trace()

test_create_issues_table()
