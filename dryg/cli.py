
import os
import argparse
import json

from dryg.table.create import create_repos_table, create_issues_table
from dryg.modelling.embedding import search_table, save_embeddings
from dryg.settings import CONFIG_URI

def cli():
    parser = argparse.ArgumentParser(description='Dryg: A minimalistic search engine for OSS')
    parser.add_argument('--init', help='Initialize the app using given username', type=str, default=None)
    parser.add_argument('--setup', help='Add a repo to the database', type=str, default=None)
    parser.add_argument('--search', help='Search for a repo', type=str, default=None)
    args = parser.parse_known_args()[0]

    if args.init:
        print(f"Initializing the app for {args.init}")
        create_repos_table(args.init)
        print(f"Run `dryg setup` to add repos to the database")
        return

    elif args.setup:
        print(f"Adding {args.setup} to the database")
        create_issues_table(args.setup)

        config = _read_config(CONFIG_URI)
        config["REPO"] = args.setup
        with open(CONFIG_URI, "w") as f:
            json.dump(config, f)

        print(f"building search space for {args.setup}")
        save_embeddings(args.setup)
        print(f"Run `dryg search` to search for issues")
        return
    
    elif args.search:
        print(f"Searching for {args.search}")
        config = _read_config(CONFIG_URI)
        if not config.get("REPO"):
            print("Run `dryg setup` to add repos to the database")
            return
        search_table(config.get("REPO") , args.search)
        return
    

# TODO: make configs project level, not user level
def _read_config(config_path):
    loaded = {}
    try:
        with open(config_path, "r") as f:
            loaded = json.load(f)
    except Exception:
        pass
    return loaded

