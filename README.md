
# 📄 DocuChat AI

**DocuChat AI** is a real-time Retrieval-Augmented Generation (RAG) application that turns static Google Docs into interactive conversations.

Powered by **Groq's Llama-3** and **LangChain**, it allows users to paste a document link and instantly ask questions, get summaries, and find specific details with citations—all in a secure, dark-mode optimized interface.

### 🚀 **[Click Here to Try the Live Demo](https://ragchatbot-fvf6gf4ddbvbhxelhcvkwy.streamlit.app/)**

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

## ⚙️ Local Installation & Setup

If you want to run this application locally, follow these steps:

### 1. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/Shiva27653/rag_chatbot.git
cd rag_chatbot

```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

This project requires specific libraries. Install them using:

```bash
pip install -r requirements.txt

```

### 4. Set Up Environment Variables

Create a file named `.env` in the root directory and add your Groq API key:

```text
GROQ_API_KEY="gsk_..."

```

*(You can get a free key from [Groq Cloud](https://console.groq.com/keys))*

### 5. Run the App

```bash
streamlit run app.py

```

---

## 🧠 How It Works

1. **Load**: The app fetches the raw text from the provided Google Doc URL using the `requests` library.
2. **Chunk**: The text is split into manageable chunks (800 characters) using `RecursiveCharacterTextSplitter`.
3. **Embed**: Each chunk is converted into a vector embedding using the **HuggingFace** `all-MiniLM-L6-v2` model.
4. **Index**: Vectors are stored in a local **FAISS** index for efficient similarity search.
5. **Retrieve & Generate**: When a user asks a question:
* The system searches for the top 3 most relevant chunks.
* It feeds these chunks + chat history to **Llama-3**.
* The model generates a precise answer with citations.



---

**Author**: Shiva27653
**License**: MIT

```

```
