import streamlit as st
import os
import requests
import re
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    st.error(" Error: GROQ_API_KEY not found in .env file.")
    st.stop()
st.set_page_config(page_title="DocuChat AI", layout="wide")
st.markdown("""
<style>
    /* Dark Mode Styles */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #363B47;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = []
def get_google_doc_text(url):
    try:
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
        if not match:
            return None, "Invalid URL format"
        doc_id = match.group(1)
        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
        response = requests.get(export_url)
        if response.status_code in [401, 403]:
            return None, " This document is Private. Please click 'Share' > 'Anyone with the link' in Google Docs."
        
        response.raise_for_status()
        return response.text, None
    except Exception as e:
        return None, f"Error: {str(e)}"
def process_document(url):
    with st.spinner("Ingesting document..."):
        raw_text, error = get_google_doc_text(url)
        
        if error:
            st.error(error)
            return None
        if not raw_text:
            st.error("Document is empty.")
            return None
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = text_splitter.create_documents([raw_text])
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store

def get_answer(query, vector_store, chat_history):
    results = vector_store.similarity_search_with_score(query, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    PROMPT_TEMPLATE = """
    You are an intelligent AI assistant. 
    Answer the question based ONLY on the context below.

    Rules:
    1. **Adapt your length**: If the user asks for a summary, be concise. If they ask for an explanation, provide details.
    2. **No repetition**: Do not repeat the question or the answer.
    3. **Citations**: Mention specific sections if available (e.g., [Section 2.1]).
    4. **Fallbacks**: If the answer is missing, say "I couldn't find that info in the document."

    HISTORY:
    {chat_history}
    
    CONTEXT:
    {context}
    
    ---
    Question: {question}
    """
    
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-3:]])
    
    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | model
    
    response = chain.invoke({
        "context": context_text, 
        "question": query,
        "chat_history": history_text
    })
    return response.content

with st.sidebar:
    st.header(" Document Loader")
    doc_url = st.text_input("URL", label_visibility="collapsed", placeholder="https://docs.google.com/...")
    
    if st.button("Load Document", type="primary"):
        if doc_url:
            st.session_state.vector_store = process_document(doc_url)
            st.session_state.messages = [] 
            if st.session_state.vector_store:
                st.toast("Document Loaded!")
        else:
            st.warning("Paste a URL first.")
            
    st.markdown("---")
    
    if st.session_state.vector_store is not None:
        st.success("Status: **Online** ")
    else:
        st.info("Status: **Waiting for Doc** ")

st.title("DocuChat AI")

if not st.session_state.messages and not st.session_state.vector_store:
    st.markdown("#### Ready to Chat! \n Paste your Google Doc link in the sidebar to begin.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.vector_store:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response_text = get_answer(prompt, st.session_state.vector_store, st.session_state.messages)
                st.markdown(response_text)
                
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:

        st.error("Please load a document first!")
