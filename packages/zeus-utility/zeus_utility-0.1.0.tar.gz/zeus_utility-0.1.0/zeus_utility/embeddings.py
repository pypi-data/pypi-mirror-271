import requests
import json
import numpy as np
import os

def is_running_in_docker():
    # Check for the .dockerenv file
    if os.path.exists("/.dockerenv"):
        return True

    # Check if Docker's cgroup is mentioned in any part of /proc/self/cgroup
    try:
        with open("/proc/self/cgroup", "rt") as ifh:
            return "docker" in ifh.read()
    except Exception as e:
        # In case reading the cgroup file fails
        print(f"Error reading '/proc/self/cgroup': {e}")
    
    return False

DOMAIN = "localhost" if not is_running_in_docker() else "host.docker.internal"
model = None
def get_embeddings_local(queries):
    global model
    from FlagEmbedding import BGEM3FlagModel
    if model is None:
        model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
        print("Model loaded.")
    embeddings = model.encode(queries, return_dense=True, return_sparse=True, return_colbert_vecs=False)
    dense_vectors:list=embeddings['dense_vecs']
    lexical_weights:list=embeddings['lexical_weights']
    return {"dense_vectors":dense_vectors,"sparse_vectors":lexical_weights}

def get_embeddings_api(queries):
    """
    Sends queries to a FastAPI endpoint to receive embeddings.

    Args:
    - queries (list of str): A list of strings for which to fetch embeddings.

    Returns:
    - embeddings (list): Embeddings received from the API.
    """
    # The URL of the FastAPI server; adjust as necessary
    url = f"http://{DOMAIN}:8240/embeddings/"
    
    # Prepare the requests payload
    payload = {
        "queries": queries
    }
    
    # Specify that we're sending JSON data
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Convert the payload dict to a JSON-formatted string
    data = json.dumps(payload)
    
    try:
        # Make the post request to the API
        response = requests.post(url, headers=headers, data=data)
        
        # If the request was successful, extract the embeddings
        if response.status_code == 200:
            embeddings = response.json()
            embeddings["dense_vectors"]=np.array(embeddings["dense_vectors"])
            embeddings["sparse_vectors"]=np.array(embeddings["sparse_vectors"])
            return embeddings
        else:
            print(f"Failed to fetch embeddings: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def get_embeddings(queries,local=False):
    if local:
        return get_embeddings_local(queries)
    return get_embeddings_api(queries)
reranker = None
def rerank_local(pairs,limit=10):
    global reranker
    from FlagEmbedding import FlagLLMReranker,FlagReranker
    if reranker is None:
        # reranker = FlagLLMReranker('BAAI/bge-reranker-v2-gemma', use_fp16=True)
        reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
    print(pairs)
    scores = reranker.compute_score(pairs)
    combined = [(pair, scores[index]) for index, pair in enumerate(pairs)]
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    # print(scores)
    # print(pairs)
    # reranked_pairs = sorted(pairs, key=lambda x: scores[x[0]], reverse=True)
    return sorted_combined[:limit]
def rerank_api(pairs):
    """
    Sends pairs to a FastAPI endpoint to receive reranked pairs.

    Args:
    - pairs (list of str): A list of pairs for which to fetch reranked pairs.
    - limit (int): The maximum number of reranked pairs to return.

    Returns:
    - reranked_pairs (list): Reranked pairs received from the API.
    """
    # The URL of the FastAPI server; adjust as necessary
    url = f"http://{DOMAIN}:8240/rerank/"
    
    # Prepare the requests payload
    payload = {
        "pairs": pairs
    }
    
    # Specify that we're sending JSON data
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Convert the payload dict to a JSON-formatted string
    data = json.dumps(payload)
    
    try:
        # Make the post request to the API
        response = requests.post(url, headers=headers, data=data)
        
        # If the request was successful, extract the reranked pairs
        if response.status_code == 200:
            reranked_pairs = response.json()
            return reranked_pairs["sorted_pairs"]
        else:
            print(f"Failed to fetch reranked pairs: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def rerank(pairs):
    return rerank_api(pairs)
        
