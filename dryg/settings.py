import logging

DB_URI = "~/.dryg/db"
WEIGHTS_URI = "weights/"
CONFIG_URI = "dryg-config.json"
SYNC_PERIOD = 7 # days


REPO_SCHEMA = ['full_name', 'id', 'html_url', 'private', 'description']
ISSUE_SCHEMA = ["title", "labels", "html_url", "body", "created_at", "closed_at", "state", "id", "comments"]

DEFAULT_MODEL = WEIGHTS_URI + "llama-7b.bin"
