import sys
import os

# Add src to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.retrieval.vector_store import TelecomVectorStore
from src.retrieval.hybrid_search import TelecomHybridRetriever
from src.llm.qa_engine import ProceduralQAEngine
import getpass

def main():
    # Prompt for API key securely for testing purposes
    if "GROQ_API_KEY" not in os.environ:
        api_key = getpass.getpass("Enter your Groq API Key (from console.groq.com) for testing: ")
        os.environ["GROQ_API_KEY"] = api_key

    print("--- Phase 3: Connecting to existing Vector Store ---")
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
    
    if not os.path.exists(db_path):
        print("Vector DB not found! Please run test_retrieval.py first to build the DB.")
        return
        
    vs_manager = TelecomVectorStore(db_path=db_path)
    retriever = TelecomHybridRetriever(vector_store_manager=vs_manager, similarity_top_k=2)
    
    # Initialize the Engine
    qa_engine = ProceduralQAEngine(retriever_pipeline=retriever)
    
    print("\n--- Phase 4: Testing LLM Generation with Strict Prompts ---")
    
    queries = [
        {
            "prompt": "What are the exact steps to clear an interface link down?",
            "filters": {"equipment_vendor": "Nokia"}
        },
        {
            "prompt": "How do I fix a nuclear reactor core meltdown?",
            "filters": {"equipment_vendor": "Nokia"}
        }
    ]
    
    for q in queries:
        print(f"\nQUERY: '{q['prompt']}'")
        # Run generation
        response = qa_engine.query(query_str=q["prompt"], filters=q["filters"])
        
        print(f"\n<< LLM RESPONSE >>\n{response.response}")
        print("\n<< SOURCES CITED >>")
        for node in response.source_nodes:
            print(f" - Document: {node.node.metadata.get('file_name')} | Header: {node.node.metadata.get('header_path')} | Score: {node.score:.2f}")
            
if __name__ == "__main__":
    main()
