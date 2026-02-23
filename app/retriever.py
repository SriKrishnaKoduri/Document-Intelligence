from app.embeddings import embed_query

def retrieve(query, vector_store):
    query_vec = embed_query(query)
    return vector_store.search(query_vec)