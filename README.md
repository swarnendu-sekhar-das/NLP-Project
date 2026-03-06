# MTech NLP Project: Telecom Procedural QA using RAG

This is our academic project for the NLP course at IIITB. We built a Question Answering system using RAG (Retrieval-Augmented Generation) specifically for Telecom Service Restoration. 

## What Does This Project Do?
Our project tries to answer questions about fixing telecom network issues based on Standard Operating Procedures (SOPs). Instead of a general chatbot, this focuses on giving step-by-step instructions without missing anything or making things up (hallucination).

## How to Run the Project

1. Clone this repository to your local machine.
2. Make sure you have Python 3 (we tested with Python 3.10+).
3. We have a script that sets up the environment and installs libraries. Run this:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
4. After that, activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
5. Then, you can run our Streamlit web app:
   ```bash
   streamlit run src/app/main.py
   ```

## Folder Structure
- `data/`: We put our raw PDF and Markdown documents here.
- `src/data_engineering/`: Code for loading documents and breaking them into smaller chunks.
- `src/retrieval/`: Code for creating embeddings and searching through them.
- `src/llm/`: Prompts and logic for talking to the LLM.
- `src/app/`: The Streamlit web interface folder.
- `src/evaluation/`: Code to evaluate the model using RAGAS.
- `notebooks/`: Jupyter notebooks we used for testing and trials.

## Tools & Libraries Used
- **Framework:** LlamaIndex
- **Embeddings:** BAAI/bge-m3 (from SentenceTransformers)
- **Vector Database:** ChromaDB 
- **LLM Engine:** Groq API running Llama-3 (8B) 
- **Evaluation:** RAGAS
- **Frontend GUI:** Streamlit
