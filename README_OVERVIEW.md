# Project Architecture & Data Flow Overview
**MTech NLP Project: Procedural QA using RAG for Telecom Service Restoration**

Our goal was to build a highly accurate QA system that telecom engineers could use during service outages. Unlike a normal chatbot that might hallucinate or skip steps, this system is rigorously engineered to find the exact manual, extract the numbered steps, and return them perfectly.

---

## 🏗️ The High-Level Architecture
This project implements the **Retrieval-Augmented Generation (RAG)** architecture using the LlamaIndex framework. It consists of two entirely separate pipelines:
1. **The Ingestion Pipeline:** (Happens offline/once). We take raw manuals, process them intelligently, convert them into mathematically comparable vectors, and store them in a database.
2. **The Retrieval & Generation Pipeline:** (Happens in real-time). The user asks a question, we search the database for relevant manual excerpts, give those excerpts to an LLM, and force it to synthesize the answer based strictly on that context.

---

## 🌊 Flow Step 1: Data Engineering (Ingestion)
*Directory: `src/data_engineering/`*

You can't just feed a 500-page telecom manual into an AI; it won't fit within the context window, and it will get easily confused.

1. **Parsing (`parser.py`)**: We use `SimpleDirectoryReader` to load the raw `.md` (or `.pdf`) manuals from the `data/` folder.
2. **Metadata Extraction (`chunking.py`)**: We pass the documents through a custom `TelecomMetadataExtractor`. Using Python Regex, it scans the text looking for specific keywords (like `ALARM_CODE_404` or `Vendor: Nokia`) and tags the document chunk with that invisible metadata.
3. **Structural Chunking (`chunking.py`)**: This is our academic novelty. Instead of slicing the document arbitrarily every 500 words (which might split Step 3 and Step 4 of a procedure across two different chunks), we use `MarkdownNodeParser`. This splits the document explicitly based on Markdown Headers (like `## Procedure`). This guarantees a contiguous procedure is kept perfectly intact inside one "node".

## 🌊 Flow Step 2: Vectorization & Storage
*Directory: `src/retrieval/`*

Now we have hundreds of perfectly chunked, metadata-tagged "Nodes" of text.

1. **Embedding Model (`embeddings.py`)**: We pass every node through a local HuggingFace embedding model (`BAAI/bge-m3`). This AI reads the English text and converts the semantic meaning of the chunk into a dense mathematical array (a vector).
2. **Vector Store (`vector_store.py`)**: We save both the raw text chunk and its mathematical vector into **ChromaDB**, which runs locally in the `chroma_db/` folder on your hard drive. 

## 🌊 Flow Step 3: The User Query & Hybrid Retrieval
*Directory: `src/retrieval/hybrid_search.py`*

The user opens Streamlit and types: *"How do I fix optical loss ALARM_501 on a Cisco router?"*

1. **The Problem with Pure Vectors**: If we just search ChromaDB mathematically for that sentence, it might accidentally return a manual for a *Nokia* router, just because the words are similar. 
2. **Hybrid Search**: To solve this, we built a `TelecomHybridRetriever`. Before searching the vectors, we apply an **Exact Metadata Filter**. We tell ChromaDB: *"Only search within chunks tagged with `vendor: Cisco` and `alarm: 501`"*. 
3. **Semantic Similarity**: Once filtered down to only Cisco 501 documents, it converts the user's question into a mathematical vector, compares it to the database, and retrieves the Top-2 most mathematically relevant chunks.

## 🌊 Flow Step 4: Generation (LLM Orchestration)
*Directory: `src/llm/`*

We now have the user's question, and the exact 2 paragraphs from the manual that contain the answer. 

1. **The LLM (`generator.py`)**: We initialize Groq's free API using the `llama-3.1-8b-instant` model. Crucially, we set `temperature = 0.0`. Temperature controls creativity. By setting it to 0, we force the AI to be robotic, deterministic, and unimaginative, severely limiting its ability to hallucinate.
2. **The Prompt Template (`prompts.py`)**: We don't just ask the LLM the question. We format a massive, strict prompt: 
   *"You are a strict telecom assistant. Here is the context: [Insert Retrieved Chunks]. Answer the user's question using ONLY this context. Format it as numbered steps. If the answer is not in the context, say 'I cannot find the procedure'."*
3. **The Engine (`qa_engine.py`)**: The `ProceduralQAEngine` wraps the Retriever and the LLM together, executes the pipeline, and spits out the final synthesized string.

## 🌊 Flow Step 5: Web UI & Evaluation
*Directory: `src/app/main.py` & `notebooks/evaluation_ragas.ipynb`*

1. **Streamlit UI**: This provides a graphical interface. It maintains a session state (chat history) and contains a sidebar where the engineer can explicitly select the Metadata Filters before asking the question. We explicitly parse the `source_nodes` from the response and print them to the screen so the user can verify the text wasn't hallucinated.
2. **RAGAS Evaluation**: For the academic report, we wrote a test dataset of Questions and Ground Truth Answers. We use the RAGAS framework to run our QA engine and mathematically compare its output to the Ground Truth, returning a grading matrix on metrics like **"Faithfulness"** and **"Answer Relevance"**.
