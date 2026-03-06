import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document

class TelecomDocumentParser:
    """
    Handles reading multiple formats of SOPs and returning a consistent format
    for downstream chunking.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        
    def load_documents(self) -> list[Document]:
        """Load Markdown and PDFs from the data directory."""
        if not os.path.exists(self.data_dir):
            print(f"Directory {self.data_dir} not found.")
            return []
            
        print(f"Loading documents from {self.data_dir}...")
        reader = SimpleDirectoryReader(
            input_dir=self.data_dir,
            recursive=True,
            required_exts=['.md', '.pdf'] 
        )
        documents = reader.load_data()
        print(f"Successfully loaded {len(documents)} document pages/files.")
        return documents
