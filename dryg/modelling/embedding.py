import logging
import pyarrow as pa
import pyarrow.compute as pc

from llama_cpp import Llama
from dryg.settings import DEFAULT_MODEL
from dryg.db import open_table, create_table
from lancedb.embeddings import with_embeddings

MODEL = None

def get_code_blocks(body: pa.ChunkedArray):
    """
    Get code blocks from the body of an issue

    Args:
        body (str): Body of the issue

    Returns:
        list: List of code blocks
    """
    code_blocks = []
    for body_chunk in body:
        if body_chunk is None:
            continue
        code_blocks += str(body_chunk).split("```")[1::2]
    return code_blocks


def setup_model(model_name:str = None):
    """
    Set the model to be used for embedding
    """
    global MODEL

    if model_name is None:
        model_name = DEFAULT_MODEL
    
    if model_name.endswith(".bin"):
        MODEL = Llama(model_name, embedding=True, n_threads=8) # workers=8 hardcoded for now
    else:
        raise ValueError("Invalid model format")

def embedding_func(batch):
    """
    Embedding function for the model
    """
    if MODEL is None:
        setup_model()
    return [MODEL.embed(x) for x in batch]

def save_embeddings(issue_table: str, force: bool = False):
    """
    Create an index for the issue table
    """
    issues = open_table(issue_table).to_arrow()
    if "vector" in issues.column_names and not force:
        logging.info("Embeddings already exist. Use `force=True` to overwrite")
        return

    issues = with_embeddings(embedding_func, issues, "title") # Turn this into a Toy problem
    create_table(issue_table, issues, mode="overwrite")

def search_table(table: str, query: str):
    """
    Search issues in the issue table

    Args:
        issue_table (str): Name of the issue table
        query (str): Query to search for

    Returns:
        list: List of issues
    """
    issues = open_table(table)
    query_embedding = embedding_func([query])[0]
    
    res =  issues.search(query_embedding).limit(10)
    import pdb; pdb.set_trace()