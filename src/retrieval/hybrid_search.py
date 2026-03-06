from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

class TelecomHybridRetriever:
    """
    Implements a Hybrid Search strategy. 
    It combines Dense Vector Search (for semantic understanding) with 
    Metadata Pre-filtering (Exact Match) to ensure that exact Error Codes
    are never missed.
    """
    def __init__(self, vector_store_manager, similarity_top_k: int = 2):
        self.index = vector_store_manager.get_index()
        self.similarity_top_k = similarity_top_k
        
    def get_retriever(self, filters: dict = None):
        """
        Creates and returns a retriever based on optional metadata filters.
        `filters` is expected to be a dict of exact matches, e.g.:
        {"equipment_vendor": "Nokia", "alarm_code": "404"}
        """
        
        # Build Metadata filters if provided
        llama_filters = None
        if filters:
            filter_params = [
                ExactMatchFilter(key=k, value=v) 
                for k, v in filters.items()
            ]
            llama_filters = MetadataFilters(filters=filter_params)
            
        # Return base Vector Retriever
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.similarity_top_k,
            filters=llama_filters
        )
        return retriever
        
    def search(self, query: str, filters: dict = None):
        """
        Convenience method to retrieve nodes for a given query and filters.
        """
        retriever = self.get_retriever(filters)
        return retriever.retrieve(query)
