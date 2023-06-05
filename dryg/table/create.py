'''
This module contains functions for syncing the database with the remote. All functions that operate on the database,
return the DB connection so that they can be chained together. This is a design choice that I'm not sure about.
'''

import datetime
import logging
import pyarrow as pa
import lancedb

from dryg.git.get import get_all_repos, get_issues, get_repo_names_ending_with
from dryg.settings import REPO_SCHEMA, ISSUE_SCHEMA, SYNC_PERIOD
from dryg.db import open_table, create_table, connection

def create_repos_table(sync: str = "auto") -> lancedb.LanceDBConnection:
    """
    Create a table with all the repos for the user

    Args:
        sync (str, optional): Whether to sync the table with the remote. Accepts "force" and "auto", defaults to "auto".
                            If set to "auto", the table is synced only if it's older than SYNC_PERIOD days.
    Returns:
        lancedb.LanceDBConnection: LanceDBConnection object
    """
    repos = open_table('repos')
    if repos:
        last_sync = repos.list_versions()[-1]['timestamp']
        days_diff = (datetime.datetime.now() - last_sync).days
        if days_diff < SYNC_PERIOD and sync == "auto": # maybe 'sync' should be a boolean?
            logging.info(f"Using cached repos, last synced {days_diff} days ago.")
            return connection()
        logging.info(f"Syncing repos, last synced {days_diff} days ago.")

    else:
        logging.info("Coudn't load repos table, creating one.")

    repos = get_all_repos()
    cols = [[] for _ in REPO_SCHEMA]
    for repo in repos:
        for idx, key in enumerate(REPO_SCHEMA):
            cols[idx].append(repo.__dict__["_rawData"][key])

    table = pa.table(cols, names=REPO_SCHEMA)
    db = create_table('repos', table)
    return db # I can return the table instead of the db object??

def create_issues_table(repo_name: str, sync: str = "auto", limit: int = 20) -> lancedb.LanceDBConnection:
    """
    Sync the issues table with the remote. Syncs all occurrences of the repo_name in the repos table inlcusing forks on other
    orgs.

    Args:
        repo_name (str): Name of the repo
        sync (str, optional): Whether to sync the table with the remote. Accepts "force" and "auto", defaults to "auto".
                            If set to "auto", the table is synced only if it's older than SYNC_PERIOD days.
    Returns:
        lancedb.LanceDBConnection: LanceDBConnection object
    """
    issues = open_table(repo_name)

    if issues:
        last_sync = issues.list_versions()[-1]['timestamp']
        days_diff = (datetime.datetime.now() - last_sync).days
        if days_diff < SYNC_PERIOD and sync == "auto":
            logging.info(f"Using cached issues, last synced {days_diff} days ago.")
            return connection()
        logging.info(f"Syncing issues, last synced {days_diff} days ago.")

    else:
        logging.info("Coudn't load issues table, creating one.")
    repos = get_repo_names_ending_with(repo_name)
    issues_list = [get_issues(repo) for repo in repos]
    cols = [[] for _ in ISSUE_SCHEMA] # combine all issues across forks into one table
    
    lim = 0
    for issues in issues_list:
        for issue in issues:
            for idx, key in enumerate(ISSUE_SCHEMA):
                cols[idx].append(issue.__dict__["_rawData"][key])
            lim += 1
            if lim >= limit:
                break
            
    table = pa.table(cols, names=ISSUE_SCHEMA)
    db = create_table(repo_name, table)

    return db
    
