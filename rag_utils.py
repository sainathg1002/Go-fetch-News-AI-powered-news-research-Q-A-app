import requests
import faiss
import numpy as np
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from groq_llm import ask_groq

# Load embedding model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- URL LOADER ---------------- #
def fetch_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # Remove junk elements
        for tag in soup(["script", "style", "noscript",
                         "header", "footer", "nav",
                         "aside", "form", "iframe"]):
            tag.decompose()

        # Priority 1: article tag
        article = soup.find("article")
        if article:
            text = article.get_text(separator=" ", strip=True)
        else:
            # Priority 2: paragraphs
            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs)

        # Priority 3: fallback to body
        if len(text) < 500:
            body = soup.find("body")
            if body:
                text = body.get_text(separator=" ", strip=True)

        return text.strip()

    except Exception:
        return ""


# ---------------- TEXT CHUNKING ---------------- #
def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


# ---------------- FAISS INDEX ---------------- #
def build_faiss(chunks):

    embeddings = embedder.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


# ---------------- RAG QUERY ---------------- #
def rag_query(question, chunks, sources, index, api_key, k=50):

    q_emb = embedder.encode(
        [question],
        normalize_embeddings=True
    ).astype("float32")

    _, idxs = index.search(q_emb, k)

    context = []
    used_sources = set()
    source_count = {}

    for idx in idxs[0]:
        src = sources[idx]

        # Limit max 5 chunks per source
        if source_count.get(src, 0) >= 5:
            continue

        context.append(chunks[idx])
        used_sources.add(src)
        source_count[src] = source_count.get(src, 0) + 1

    prompt = f"""
You are an analytical assistant.

Answer the question using ONLY the context below.
If the answer is not present, say:
"The information is not available in the provided sources."

Context:
{" ".join(context)}

Question:
{question}

Answer:
"""

    answer = ask_groq(prompt, api_key)
    return answer, list(used_sources)
