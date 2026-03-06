import sys
import os

from llama_index.core.schema import TextNode

# Add src to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.data_engineering.parser import TelecomDocumentParser
from src.data_engineering.chunking import get_procedural_chunker, TelecomMetadataExtractor


class DataPipeline:
    def __init__(self, data_dir: str):
        self.parser = TelecomDocumentParser(data_dir=data_dir)
        self.chunker = get_procedural_chunker()
        self.metadata_extractor = TelecomMetadataExtractor()

    def run(self) -> list[TextNode]:
        """
        1. Loads Documents
        2. Applies Structural Markdown Chunking
        3. Extracts and Attaches Telecom Metadata
        """
        print("--- Starting Data Pipeline ---")
        docs = self.parser.load_documents()
        if not docs:
            print("No documents found. Aborting pipeline.")
            return []

        print("Chunking documents structually (by headers)...")
        nodes = self.chunker.get_nodes_from_documents(docs)
        print(f"Produced {len(nodes)} structural chunks.")

        print("Extracting metadata...")
        # Since we are using an async-compatible extractor from LlamaIndex BaseExtractor, 
        # we can just run our custom synchronous extraction logic over the nodes directly for this demo
        for node in nodes:
            metadata = self.metadata_extractor._extract_metadata(node.get_content())
            # Safely merge extracted dict into the node's existing metadata
            node.metadata.update(metadata)

        print("--- Data Pipeline Finished ---")
        return nodes
