import sys
import os

# Add src to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_engineering.pipeline import DataPipeline
from src.retrieval.vector_store import TelecomVectorStore
from src.retrieval.hybrid_search import TelecomHybridRetriever

def main():
    print("--- Phase 2: Loading & Chunking Data ---")
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    pipeline = DataPipeline(data_dir=data_dir)
    nodes = pipeline.run()
    
    # Optional: Filter out empty nodes if any appeared due to formatting
    clean_nodes = [n for n in nodes if n.get_content().strip()]

    print("\n--- Phase 3: Initializing Vector Store ---")
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
    
    # Make sure to clear previous testing DBs to avoid dupes across script runs
    if os.path.exists(db_path):
        import shutil
        print(f"Clearing old DB at {db_path} for clean test...")
        shutil.rmtree(db_path)
        
    vs_manager = TelecomVectorStore(db_path=db_path)
    
    # Embed and Insert Nodes into Chroma
    vs_manager.insert_nodes(clean_nodes)
    
    print("\n--- Phase 3: Testing Hybrid Search Retrieval ---")
    retriever = TelecomHybridRetriever(vector_store_manager=vs_manager, similarity_top_k=2)
    
    queries = [
        {
            "prompt": "How do I fix optical Rx loss on my Nokia router?",
            "filters": {"equipment_vendor": "Nokia"}
        },
        {
            "prompt": "Wait, I have an alarm 404, what are the steps?",
            "filters": {"alarm_code": "404"}
        }
    ]
    
    for q in queries:
        print(f"\nQUERY: '{q['prompt']}' | FILTERS: {q['filters']}")
        results = retriever.search(query=q["prompt"], filters=q["filters"])
        
        for i, node_with_score in enumerate(results):
            score = node_with_score.score
            node = node_with_score.node
            print(f"  -> Result {i+1} (Score/Similarity: {score:.4f}):")
            print(f"     Title/Header: {node.metadata.get('header_path', 'No Header')}")
            preview = node.get_content()[:120].replace('\n', ' ')
            print(f"     Content: {preview}...")
            print(f"     Metadata: {node.metadata}")

if __name__ == "__main__":
    main()
