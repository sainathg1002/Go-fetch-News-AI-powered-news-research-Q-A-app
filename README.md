<<<<<<< HEAD
﻿# 🚀 GoFetch – AI-Powered News Research & Q&A Tool

I recently built a Streamlit-based intelligent research assistant that leverages Retrieval-Augmented Generation (RAG) to answer questions from multiple web sources with high accuracy and speed.

## ✨ Features

🔹 **🌐 Multi-Source Web Scraping**: Automatically extracts and processes content from multiple URLs simultaneously, intelligently parsing article content while filtering out navigation, scripts, and irrelevant elements.

🔹 **🧠 Semantic Search with FAISS**: Uses vector embeddings and FAISS indexing for lightning-fast similarity search, retrieving the most relevant context chunks to answer user queries accurately.

🔹 **⚡ Groq LLM Integration**: Powered by Groq's ultra-fast LLM API (llama-3.1-8b-instant) for low-latency, high-quality responses with minimal hallucination.

🔹 **📊 Source Attribution**: Tracks and displays source URLs for every answer, ensuring transparency and verifiability of information.

🔹 **🎨 Modern UI/UX**: Clean, responsive interface with gradient buttons, smooth animations, and a professional dark-themed design built with custom CSS.

🔹 **🔄 Smart Context Balancing**: Implements source diversity logic to prevent over-reliance on a single URL, ensuring balanced and comprehensive answers.

## 🛠️ Tech Stack

- **Python** – Core programming language
- **Streamlit** – Interactive web application framework
- **Groq API** – Ultra-fast LLM inference
- **FAISS** – Facebook AI Similarity Search for vector indexing
- **Sentence Transformers** – all-MiniLM-L6-v2 for text embeddings
- **BeautifulSoup4** – Web scraping and HTML parsing
- **Requests** – HTTP library for fetching web content

## 🧠 Key Learnings

This project deepened my understanding of:
- Building production-ready RAG pipelines with semantic retrieval
- Optimizing vector search with FAISS for real-time performance
- Web scraping strategies for clean content extraction
- Prompt engineering for accurate, context-aware LLM responses
- Creating intuitive UIs for AI applications with Streamlit

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd notebook
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

4. Run the application:
```bash
streamlit run app.py
```

## 📖 How It Works

1. **Input URLs**: Enter up to 3 news article URLs
2. **Processing**: The system scrapes, chunks, and indexes the content
3. **Ask Questions**: Query the knowledge base with natural language
4. **Get Answers**: Receive accurate, source-attributed responses in seconds

## 🎯 Use Cases

- 📰 News research and fact-checking
- 📚 Academic research across multiple sources
- 🔍 Competitive intelligence gathering
- 📊 Market research and trend analysis

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---
📝 Note

This project is built for learning, experimentation, and showcasing GenAI system design using real-world data and fast LLM inference.

**Built by Venkata Sai** • AI & Full Stack Enthusiast
=======
