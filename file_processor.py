import os
import shutil
import logging
import streamlit as st
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from src.document_processor import process_document, extract_text_from_webpage, split_documents
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Paths
UPLOAD_DIR = "uploaded_files"
FAISS_INDEX_PATH = "faiss_index"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def clear_embeddings():
    """Clear all existing embeddings."""
    if os.path.exists(FAISS_INDEX_PATH):
        shutil.rmtree(FAISS_INDEX_PATH)  # Recursively delete the directory
        os.makedirs(FAISS_INDEX_PATH, exist_ok=True)  # Recreate the directory
    logging.info("FAISS index cleared.")

def process_and_store_embeddings(documents):
    """Process the input documents and store embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please set it before running this process.")

    embeddings = OpenAIEmbeddings()

    # Check if FAISS index already exists
    if os.path.exists(FAISS_INDEX_PATH) and os.listdir(FAISS_INDEX_PATH):
        logging.info("FAISS index already exists. Clearing before new embeddings.")
        clear_embeddings()

    # Process chunks in batches for embeddings
    vectorstore = None
    batch_size = 50  # Number of chunks per batch
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        if vectorstore is None:
            vectorstore = FAISS.from_documents(batch, embeddings)
        else:
            vectorstore.add_documents(batch)

    vectorstore.save_local(FAISS_INDEX_PATH)
    logging.info(f"Embeddings created and saved to {FAISS_INDEX_PATH}.")

def summarize_documents(documents):
    """Summarize the given documents in chunks."""
    llm = ChatOpenAI(temperature=0.7)
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summaries = []
    chunk_size = 50  # Number of chunks per summarization batch
    for i in range(0, len(documents), chunk_size):
        batch = documents[i:i + chunk_size]
        summaries.append(chain.run(batch))

    return "\n".join(summaries)

# Streamlit Interface


st.set_page_config(page_title="TekRevol HR Knowledgebase", page_icon="🤖")
st.title("TekRevol HR Chatbot")
st.markdown("""
Welcome to the TekRevol HR Knowledgebase Chatbot! 🤖

This chatbot provides quick answers about company policies, training materials, rate cards, leadership information, and more. Simply upload documents or enter a URL to get started.
""")


# Sidebar for API key input
with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# Input Options
input_option = st.radio("Choose Input Method:", ("Upload Files", "Enter URLs"))
task_option = st.radio("Choose Task:", ("Ask Questions", "Summarize"))

if input_option == "Upload Files":
    uploaded_files = st.file_uploader("Upload files for processing", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        if st.button("Process Files"):
            if api_key:
                with st.spinner("Processing files..."):
                    documents = []
                    try:
                        for uploaded_file in uploaded_files:
                            # Save each uploaded file temporarily
                            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            # Process each document and append chunks
                            documents.extend(split_documents(process_document(file_path)))
                            os.remove(file_path)

                        if task_option == "Summarize":
                            summary = summarize_documents(documents)
                            st.subheader("Summary:")
                            st.write(summary)
                        else:
                            process_and_store_embeddings(documents)
                            st.success("Files processed and embeddings saved successfully!")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.error("Please provide your OpenAI API key.")

elif input_option == "Enter URLs":
    urls = st.text_area("Enter URLs (one per line):")
    if urls.strip() and st.button("Process URLs"):
        if api_key:
            with st.spinner("Processing URLs..."):
                documents = []
                try:
                    for url in urls.strip().splitlines():
                        # Extract text from each URL and append chunks
                        documents.extend(split_documents(extract_text_from_webpage(url)))

                    if task_option == "Summarize":
                        summary = summarize_documents(documents)
                        st.subheader("Summary:")
                        st.write(summary)
                    else:
                        process_and_store_embeddings(documents)
                        st.success("URLs processed and embeddings saved successfully!")
                except Exception as e:
                    st.error(str(e))
        else:
            st.error("Please provide your OpenAI API key.")

# Clear embeddings
if st.button("Clear Embeddings"):
    try:
        clear_embeddings()
        st.success("FAISS index cleared successfully!")
    except Exception as e:
        st.error(f"Error clearing embeddings: {e}")
