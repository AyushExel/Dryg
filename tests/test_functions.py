import lancedb

from dryg.settings import REPO_SCHEMA
from dryg.git.get import get_all_repos, get_issues, get_repo_by_name
from dryg.table.sync import create_repo_table

CACHE = {} # This is a hack to avoid making too many calls to the api

def test_get_repos():
    repos = get_all_repos()
    assert isinstance(repos, list), "Expected list of repos"
    CACHE['repos'] = repos

def test_get_issues():
    repos = CACHE.get("repos") or get_all_repos()
    issues = get_issues(repos[0])
    assert isinstance(issues, list), "Expected list of issues"

'''
TODO: Fix this test
def test_get_repo_by_name():
    repo = get_repo_by_name("ultralytics")
    assert isinstance(repo, github.Repository.Repository), "Expected repo object"
'''

def test_create_repo_table():
    db = create_repo_table()
    assert isinstance(db, lancedb.LanceDBConnection), "Expected LanceDBConnection"
    repos = db.open_table('repos')
    assert repos.schema.names == REPO_SCHEMA, "Expected schema to match REPO_SCHEMA"
