📰 Go-Fetch-News
AI-Powered News Research & Q&A App

Go-Fetch-News is an AI-powered news research and question-answering application that allows users to fetch news articles from the web and ask natural language questions based on the retrieved content.

The system combines web data ingestion + LLM reasoning to deliver context-aware answers, making it useful for market research, current affairs analysis, and content exploration.

🏗️ Architecture Overview

The application follows a pipeline-based, agent-style architecture:

News Fetcher Module

Retrieves news articles from provided URLs or predefined sources

Cleans and structures raw article content

Text Chunking & Processing

Splits long news articles into manageable chunks

Prepares data for efficient LLM reasoning

LLM Reasoning Layer

Uses the Groq API for fast and low-latency LLM inference

Performs question answering over the processed news content

Prompt Handler

Accepts user questions in natural language

Injects relevant context into the LLM prompt

Response Generator

Produces concise, source-aware answers

Ensures responses are grounded in fetched news data

🧰 Tech Used
🧠 AI & LLM

Groq API – High-speed LLM inference for news understanding and question answering

Large Language Models (LLMs) – Used for contextual reasoning over fetched news content

🐍 Backend & Core Logic

Python – Core application logic and orchestration

Agent-style pipeline – Modular flow for fetching, processing, and answering

🌐 Data Ingestion

Web Scraping / Article Extraction – Fetches and cleans news content from URLs

HTML Parsing – Extracts readable text from web pages

🧩 Text Processing

Text Chunking – Splits long articles into manageable chunks for LLM context handling

Context Injection – Injects relevant article chunks into LLM prompts

🔐 Configuration & Environment

dotenv (.env) – Secure API key management

Environment variables – Keeps secrets out of source code

📦 Dependency Management & Execution

uv – Fast Python package installer

pip / requirements.txt – Dependency specification

CLI-based execution – Run via python main.py

🧪 Development Practices

Modular code structure – Easy to extend and maintain

Prompt engineering – Carefully structured prompts for grounded answers

Error handling & validation – Basic runtime checks for stability

🔑 One-Line Summary (Resume-Ready)

Go-Fetch-News is built using Python and Groq-powered LLM inference, combining web data ingestion, text chunking, and prompt-based reasoning to deliver fast, context-aware news Q&A.

📥 How to Download the Project

Clone the repository from GitHub:

git clone https://github.com/your-username/Go-fetch-News-AI-powered-news-research-Q-A-app.git
cd Go-fetch-News-AI-powered-news-research-Q-A-app

🔐 Environment Setup

Create a .env file in the project root:

GROQ_API_KEY=your_api_key_here


⚠️ Never commit your .env file to GitHub.
Refer to .env.example for required environment variables.

📦 Install Dependencies (Using uv)

Ensure uv is installed:

pip install uv


Install project dependencies:

uv pip install -r requirements.txt

▶️ How to Run the Project

After completing all installations, start the application:

python main.py

Usage Flow

Enter one or more news article URLs

Allow the app to fetch and process the content

Ask natural language questions based on the fetched news

Receive context-aware AI-generated answers

Example question:

Why are liquid cooling systems gaining popularity in data centers?

🎯 Project Goals

Build a practical AI-powered research assistant

Explore real-world LLM context injection

Demonstrate fast inference using Groq API

Design a clean, modular data-to-answer pipeline

🚀 Future Improvements

Multi-source citation support

Advanced relevance filtering

UI integration (Streamlit / Web)

Persistent vector storage

📝 Note

This project is built for learning, experimentation, and showcasing GenAI system design using real-world data and fast LLM inference.

