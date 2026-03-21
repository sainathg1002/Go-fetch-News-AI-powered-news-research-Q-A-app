# 🔍 Go Fetch — RAG-Based News Research System

> Ask any question. Get answers grounded in real news sources — not hallucinations.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-green.svg)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-LLM%20API-orange.svg)](https://groq.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-red.svg)](https://faiss.ai)

---

## What Is This?

Go Fetch is a **Retrieval-Augmented Generation (RAG)** system that answers questions using real news articles — not the LLM's memory.

You give it a question → it fetches relevant news → retrieves the most relevant chunks → generates a grounded answer with sources.

**No hallucinations. Every answer is backed by actual articles.**
**Live Link**: https://sainathg1002-go-fetch-news-ai-powered-news-research--app-ldv2kp.streamlit.app/

---

## How It Works

```
Your Question
     │
     ▼
┌─────────────────┐
│  News Fetcher   │  ← Pulls articles from news sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAISS Index    │  ← Breaks articles into chunks, stores as vectors
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Smart Retrieval │  ← Finds top 50 relevant chunks,
│  (k=50, cap=5)  │    balanced across multiple sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Groq LLM      │  ← Generates answer using only retrieved context
└────────┬────────┘
         │
         ▼
  Answer + Sources
```

**Key design decision:** The retriever caps at 5 chunks per source. This prevents one dominant article from controlling the answer — giving you balanced, multi-perspective responses.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph |
| LLM | Groq API (LLaMA-3) |
| Vector Search | FAISS |
| Embeddings | Sentence Transformers |
| Backend | Python, FastAPI |
| Prompt Design | Custom prompt engineering |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/go-fetch.git
cd go-fetch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Example Usage

```
Question: "What are the latest developments in AI regulation?"

→ Fetches 10 relevant news articles
→ Chunks and indexes them into FAISS
→ Retrieves top 50 relevant chunks (max 5 per article)
→ Groq LLM synthesizes a grounded answer

Answer: "According to Reuters (2026), the EU AI Act enforcement 
began in Q1... Meanwhile, Bloomberg reports that the US Senate..."
```

---

## Project Structure

```
go-fetch/
├── app.py                  # Streamlit UI
├── rag_pipeline.py         # Core RAG logic
├── retriever.py            # FAISS indexing + smart retrieval
├── news_fetcher.py         # Article fetching
├── prompts.py              # Prompt templates
├── requirements.txt
└── .env.example
```

---

## Why This Is Different From a Basic RAG

| Basic RAG | Go Fetch |
|---|---|
| Simple top-k retrieval | Balanced multi-source retrieval |
| Single source dominates | 5-chunk cap per source |
| No orchestration | LangGraph state machine |
| Slow retrieval | <1s latency |

---

## Requirements

```
Python 3.10+
langchain
langgraph
groq
faiss-cpu
sentence-transformers
streamlit
fastapi
python-dotenv
```

---

## Author

**Venkata Sainath Ganta**
[GitHub](https://github.com/sainathg1002) • [LinkedIn](https://www.linkedin.com/in/venkata-sai-ganta-c300b200a100/) • [Portfolio](https://sainathg1002.github.io/sainath_portfolio/)
