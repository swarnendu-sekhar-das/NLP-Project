from llama_index.core.query_engine import RetrieverQueryEngine
from src.llm.generator import get_llm_generator
from src.llm.prompts import procedural_qa_prompt

class ProceduralQAEngine:
    """
    Ties together the Vector Retriever (Phase 3) and the LLM 
    (Phase 4) into a cohesive Question-Answering pipeline.
    """
    
    def __init__(self, retriever_pipeline):
        """
        Expects an instance of TelecomHybridRetriever from Phase 3.
        """
        self.retriever = retriever_pipeline
        self.llm = get_llm_generator()
        
    def query(self, query_str: str, filters: dict = None) -> str:
        """
        1. Fetch chunks from ChromaDB using Vector + Metadata filters.
        2. Give chunks + query to strict PromptTemplate.
        3. LLM Generates Final Answer.
        """
        
        # Get the configured LlamaIndex Retriever from our wrapper
        base_retriever = self.retriever.get_retriever(filters)
        
        # Build the Query Engine
        engine = RetrieverQueryEngine.from_args(
            retriever=base_retriever,
            llm=self.llm,
            text_qa_template=procedural_qa_prompt
        )
        
        # Execute query
        response = engine.query(query_str)
        
        # Return object containing text and source nodes (citations)
        return response
