import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()

# Path to FAISS index
FAISS_INDEX_PATH = "faiss_index"

def load_vectorstore():
    """Load the FAISS index."""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError("FAISS index not found. Please process and save embeddings first.")
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

# Initialize Streamlit App
st.set_page_config(page_title="TekRevol HR Knowledgebase", page_icon="💬")
st.title("TekRevol HR Chatbot")
st.markdown("""
Welcome to the **TekRevol HR Chatbot**, your **TekRevol Assistant**! 💬  

I can assist with questions about company policies, training materials, rate cards, leadership information, and more. Ask away or provide a document/URL for analysis.
""")



# Sidebar for API key input
with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# Initialize session state
if "messages" not in st.session_state:
    # Initialize session state with the introduction message
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I’m your TekRevol Assistant! 🤖 How can I assist you today? You can ask about company policies, training, rate cards, leadership, or upload documents for analysis."
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if "rag_chain" not in st.session_state:
    try:
        # Load FAISS index and create retriever
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever()

        # Create RAG Chain
        st.session_state.rag_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.7),
            retriever=retriever
        )
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")



# User input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant's response
    if api_key:
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Convert chat history to expected format (list of tuples)
                    chat_history = [
                        (m["content"], st.session_state.messages[idx + 1]["content"])
                        for idx, m in enumerate(st.session_state.messages[:-1])
                        if m["role"] == "user" and idx + 1 < len(st.session_state.messages)
                    ]

                    result = st.session_state.rag_chain({
                        "question": prompt,
                        "chat_history": chat_history,
                    })

                    response = result["answer"]
                    st.markdown(f"**TekRevol Assistant:** {response}")

            # Add assistant's response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please provide your OpenAI API key.")
