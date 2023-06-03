'''
This module contains functions for syncing the database with the remote. All functions that operate on the database,
return the DB object so that they can be chained together. This is a design choice that I'm not sure about.
'''

import datetime
import logging
import pyarrow as pa
import lancedb

from dryg.git.get import get_all_repos, get_issues, get_repo_by_name
from dryg.settings import DB_URI, REPO_SCHEMA, SYNC_PERIOD

def create_repo_table():
    db = lancedb.connect(DB_URI)
    try:
        repos = db.open_table('repos')
        last_sync = repos.list_versions()[-1]['timestamp']
        days_diff = (datetime.datetime.now() - last_sync).days
        if days_diff < SYNC_PERIOD:
            logging.info(f"Using cached repos, last synced {days_diff} days ago.")
            return db
        logging.info(f"Syncing repos, last synced {days_diff} days ago.")

    except ValueError:
        logging.info("Coudn't load repos table, creating one.")

    repos = get_all_repos()
    cols = [[] for _ in REPO_SCHEMA]
    for repo in repos:
        for idx, key in enumerate(REPO_SCHEMA):
            cols[idx].append(repo.__dict__["_rawData"][key])

    table = pa.table(cols, names=REPO_SCHEMA)
    db = lancedb.connect(DB_URI)
    db.create_table('repos', table, mode="overwrite")
    return db # I can return the table instead of the db object??
    