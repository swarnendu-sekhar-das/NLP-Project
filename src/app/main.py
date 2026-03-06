import streamlit as st
import os
import sys

# Ensure the src module is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.retrieval.vector_store import TelecomVectorStore
from src.retrieval.hybrid_search import TelecomHybridRetriever
from src.llm.qa_engine import ProceduralQAEngine

# Configure the Streamlit page
st.set_page_config(
    page_title="Telecom QA RAG",
    page_icon="📡",
    layout="wide",
)

# Initialize the QA Engine once and store it in session state
@st.cache_resource
def load_qa_engine(api_key: str = None):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db"))
    if not os.path.exists(db_path):
        return None
    
    # We must set the Env variable here immediately so LlamaIndex picks it up during initialization
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        
    vs_manager = TelecomVectorStore(db_path=db_path)
    retriever = TelecomHybridRetriever(vector_store_manager=vs_manager, similarity_top_k=2)
    return ProceduralQAEngine(retriever_pipeline=retriever)

# Header Information
st.title("📡 Procedural QA for Telecom Service Restoration")
st.markdown("""
This system uses Retrieval-Augmented Generation (RAG) to find and output the exact Standard Operating Procedures (SOPs) for telecom service restoration.
It uses hybrid search and semantic chunking to ensure procedural steps are kept intact without skipping or hallucinating.
""")


if "GROQ_API_KEY" not in os.environ and "api_key" not in st.session_state:
    # Sidebar input for API Key if not found in env
    api_key = st.sidebar.text_input("Groq API Key (Free)", type="password")
    if not api_key:
        st.warning("Please enter your Groq API Key (from console.groq.com) in the sidebar to use the free LLM.")
        st.stop()
    else:
        st.session_state.api_key = api_key
        os.environ["GROQ_API_KEY"] = api_key

# Load Engine dynamically AFTER key is set
qa_engine = load_qa_engine(st.session_state.get("api_key", os.environ.get("GROQ_API_KEY")))

if not qa_engine:
    st.error("Vector Database not found! Please run the Phase 2/3 test scripts first to index the documents.")
    st.stop()

st.divider()

# Sidebar for explicit Metadata Filtering (Mimicking Hybrid Keyword Search)
st.sidebar.header("Pre-Filtering (Hybrid Search)")
st.sidebar.markdown("Use these filters to ensure exact error codes are retrieved via Metadata Filtering, solving the issue of pure vector search missing specific model numbers.")
vendor_filter = st.sidebar.selectbox("Equipment Vendor", ["Any", "Nokia", "Cisco", "Juniper"])
alarm_filter = st.sidebar.text_input("Exact Alarm Code (e.g. 404, 501)", value="")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a clear chat button to the sidebar
if st.sidebar.button("Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Show Retrieved Context (For Academic Evaluation)"):
                for source in message["sources"]:
                    st.markdown(f"**Document:** `{source['file_name']}`  \n**Section Header:** `{source['header']}`  \n**Confidence Score:** `{source['score']:.2f}`")
                    st.text(source['text'])

# React to user input
if prompt := st.chat_input("Ask a procedural question (e.g., 'How to clear ALARM_CODE_404 on router XYZ?'): "):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare filters
    filters = {}
    if vendor_filter != "Any":
        filters["equipment_vendor"] = vendor_filter
    if alarm_filter.strip():
        filters["alarm_code"] = alarm_filter.strip()
        
    # Query Engine
    with st.chat_message("assistant"):
        with st.spinner("Retrieving SOPs and Synthesizing Answer..."):
            try:
                response = qa_engine.query(prompt, filters=filters if filters else None)
                st.markdown(response.response)
                
                # Extract Sources explicitly for grading
                source_data = []
                if response.source_nodes:
                    with st.expander("Show Retrieved Context (For Academic Evaluation)"):
                        for node in response.source_nodes:
                            file_name = node.node.metadata.get('file_name', 'Unknown')
                            header = node.node.metadata.get('header_path', 'No Header')
                            source_text = node.node.get_content()
                            score = node.score
                            
                            st.markdown(f"**Document:** `{file_name}`  \n**Section Header:** `{header}`  \n**Confidence Score:** `{score:.2f}`")
                            st.text(source_text[:500] + "...\n[TRUNCATED]")
                            
                            source_data.append({
                                "file_name": file_name,
                                "header": header,
                                "score": score,
                                "text": source_text[:500] + "...\n[TRUNCATED]"
                            })
                            
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.response, "sources": source_data})
                
            except Exception as e:
                error_msg = f"**Error:** Failed to generate response. Please check your Groq API Key.\n\n`{str(e)}`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
