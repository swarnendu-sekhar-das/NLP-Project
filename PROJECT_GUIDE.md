# Comprehensive Guide: Using, Testing, and Improving the Telecom RAG System

This guide is designed for your 4-member academic team to understand how to operate the system, how to test it for your final project report, and what future improvements each member can make to score higher marks.

---

<YOUR_GROQ_API_KEY_HERE>

## Part 1: How to Use the System

The project is structured into modular Python scripts that must be run in a specific order the very first time you add new Method of Procedure (SOP/MOP) documents.

### Step 1: Add your Documents
Place any Telecom Manuals (PDFs or Markdown files) into the `data/` folder. 
* *Currently, there is a `dummy_nokia_router_mop.md` file in there used for baseline testing.*

### Step 2: Activate the Virtual Environment
Every time you open an IDE or terminal for this project, you must activate the isolated Python environment:
```bash
source .venv/bin/activate
```

### Step 3: Run the Ingestion Pipeline (Chunking & Embedding)
Whenever you add or change a file in the `data/` folder, you must re-run the ingestion pipeline. This reads the files, chunks them structurally (by headers), applies Regex Metadata (Alarm Codes), converts them into vectors using the `BAAI/bge-m3` model, and saves them to the local `chroma_db/` directory.
```bash
python notebooks/test_retrieval.py
```
*(Wait until you see "Indexing Complete", and it will print out a test retrieval).*

### Step 4: Run the Web Application
Once the `chroma_db/` folder exists and is populated, you can launch the interactive chat UI.
```bash
streamlit run src/app/main.py
```
1. A browser window will open.
2. Enter your **Groq API Key** into the left sidebar (get one for free at `console.groq.com`).
3. Use the sidebar to optionally filter by **Vendor** or **Alarm Code**.
4. Ask a question like: *"What is the procedure to fix ALARM_CODE_501?"*

---

## Part 2: How to Test the System for Academic Grading

To prove to your professors that your system is highly accurate and doesn't hallucinate, you must use **RAGAS (Retrieval Augmented Generation Assessment)**.

1. Ensure the `.venv` is activated.
2. Start Jupyter Lab:
```bash
jupyter lab
```
3. Open `notebooks/evaluation_ragas.ipynb`.
4. Run all the cells sequentially. 
5. When prompted in the notebook, paste your Groq API Key.
6. The final cell will output a **Pandas DataFrame** containing metrics like **Faithfulness** (0 to 1 score) and **Context Precision** (0 to 1 score).
7. **Take a screenshot of this DataFrame** and put it in your final presentation slides to prove your system works objectively.

---

## Part 3: How to Make Further Improvements (By Member)

To get top marks, you should demonstrate that you didn't just use baseline RAG, but implemented advanced NLP concepts. Here is what each team member can do next:

### Member 1 (Data Engineering)
**File to modify:** `src/data_engineering/chunking.py`
**Improvements to make:**
1. **PDF Parsing:** The current parser is mostly optimized for Markdown. You should integrate `llamaParse` or `PyPDF2` to extract structured tables from Telecom PDFs. 
2. **Advanced Regex:** Update the `TelecomMetadataExtractor` to identify specifically formatted IP Address regex patterns or MAC Addresses from the documents and attach them as metadata.

### Member 2 (Core Retrieval)
**File to modify:** `src/retrieval/hybrid_search.py`
**Improvements to make:**
1. **Query Expansion (HyDE):** Before passing the user's query ("Fix my router") to the Vector DB, use a small LLM call to expand the query into a hypothetical answer ("The procedure to fix an optical loss on Nokia..."). Then vectorize the expanded query for much higher similarity scores. LlamaIndex has built-in HyDE support you can import.
2. ** BM25 Integration:** Currently, "Hybrid Search" is achieved via Exact Metadata Filtering. To make it true hybrid search, configure `ChromaDB` alongside a BM25 sparse retriever and use `Reciprocal Rank Fusion (RRF)` to merge the top results.

### Member 3 (LLM Orchestration)
**Files to modify:** `src/llm/prompts.py` and `src/llm/qa_engine.py`
**Improvements to make:**
1. **Switch to Local Models:** Currently, it uses the Groq API for `llama3`. You can install [Ollama](https://ollama.com/) on your local machine, download `llama3` (`ollama run llama3`), and swap the `Groq` class in `generator.py` for LlamaIndex's `Ollama` class. This proves you can build a 100% offline, secure system (which Telecom companies require).
2. **Strict Output Parsing:** Use `PydanticOutputParser` to force the LLM to return strictly formatted JSON `{ "alarm": "...", "steps": ["1", "2"] }` instead of a plain text string.

### Member 4 (Full-Stack & Evaluation)
**Files to modify:** `src/app/main.py` and `notebooks/evaluation_ragas.ipynb`
**Improvements to make:**
1. **Expand RAGAS Dataset:** Add 20-30 more Ground Truth Question/Answer pairs to your evaluation notebook to make the final metrics statistically significant.
2. **Chat Memory:** Currently, the Streamlit app treats every question as isolated. Import LlamaIndex's `ChatMemoryBuffer` into `qa_engine.py` so the user can ask follow-up questions like *"What was step 2 again?"* without losing context.
