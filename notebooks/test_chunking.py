import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_engineering.pipeline import DataPipeline

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    pipeline = DataPipeline(data_dir=data_dir)
    nodes = pipeline.run()

    print("\n--- Displaying Sample Chunks ---")
    for i, node in enumerate(nodes):
        print(f"\n[{i+1}/{len(nodes)}] Node Metadata: {node.metadata}")
        content_preview = node.get_content()[:200] + "..." if len(node.get_content()) > 200 else node.get_content()
        print(f"Content Preview: {content_preview}")
        print("-" * 50)

if __name__ == "__main__":
    main()
