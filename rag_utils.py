import requests
import faiss
import numpy as np
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from groq_llm import ask_groq

embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ---------- URL LOADER ----------
def fetch_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # remove junk
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        # PRIORITY 1: article tag
        article = soup.find("article")
        if article:
            text = article.get_text(separator=" ", strip=True)
        else:
            # PRIORITY 2: paragraph aggregation
            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return text.strip()

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return ""





# ---------- TEXT SPLITTER ----------
def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


# ---------- FAISS INDEX ----------
def build_faiss(chunks):
    embeddings = embedder.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index


# ---------- RETRIEVAL + GENERATION ----------
def rag_query(question, chunks, sources, index, k=8):
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

        # limit dominance of one source
        if source_count.get(src, 0) >= 2:
            continue

        context.append(chunks[idx])
        used_sources.add(src)
        source_count[src] = source_count.get(src, 0) + 1

    prompt = f"""
You are an analytical assistant.

Answer the question using the context below.
If the answer is not present, say:
"The information is not available in the provided sources."

Context:
{" ".join(context)}

Question:
{question}

Answer:
"""

    answer = ask_groq(prompt)
    return answer, list(used_sources)
