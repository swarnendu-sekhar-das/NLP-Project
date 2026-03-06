from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_embedding_model():
    """
    Initializes and returns the BAAI/bge-m3 embedding model.
    This model runs locally and is open-source.
    """
    # Using BAAI/bge-m3 as the default embedding model for this project
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    # Note: using bge-small for faster local testing in the baseline. 
    # For production/final grading, swap to model_name="BAAI/bge-m3"
    
    return embed_model
