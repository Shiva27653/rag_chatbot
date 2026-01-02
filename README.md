# 📄 DocuChat AI

**DocuChat AI** is a real-time Retrieval-Augmented Generation (RAG) application that turns static Google Docs into interactive conversations. 

Powered by **Groq's Llama-3** and **LangChain**, it allows users to paste a document link and instantly ask questions, get summaries, and find specific details with citations—all in a secure, dark-mode optimized interface.

### 🚀 **Live Demo**
[**Click here to try DocuChat AI**](https://ragchatbot-fvf6gf4ddbvbhxelhcvkwy.streamlit.app/)

---

## ⚡ Key Features

- **Instant Ingestion**: Programmatically fetches and chunks text from public Google Docs.
- **RAG Architecture**: Uses **FAISS** vector search to retrieve only the most relevant context for every query.
- **Blazing Fast Inference**: Leveraging **Groq API (Llama-3)** for near-instant responses.
- **Context-Aware Memory**: Remembers your conversation history for natural, multi-turn dialogue.
- **Smart Citations**: Every answer includes references to specific sections of the document.
- **Robust Error Handling**: Automatically detects private links and guides users to fix permissions.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Custom CSS styled)
- **LLM**: Llama-3.1-8b-Instant (via Groq)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Orchestration**: LangChain
- **Language**: Python 3.10+

---

## ⚙️ Installation & Local Setup

If you want to run this locally, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/Shiva27653/rag_chatbot.git](https://github.com/Shiva27653/rag_chatbot.git)
cd rag_chatbot
