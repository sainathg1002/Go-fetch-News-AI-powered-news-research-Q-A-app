import streamlit as st
from rag_utils import fetch_text, chunk_text, build_faiss, rag_query

st.set_page_config(
    page_title="GoFetch – News Research Tool",
    layout="centered"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* App Background */
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #fef3c7 100%);
}

/* Main Container */
.main .block-container {
    padding: 2rem 1rem;
    max-width: 900px;
}

/* Header Title */
.main-title {
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] h2 {
    color: #1e293b;
    font-weight: 600;
}

[data-testid="stSidebar"] h3 {
    color: #475569;
    font-size: 1rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    color: #64748b;
}

[data-testid="stSidebar"] .stTextInput input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.1) !important;
}

/* Content Card */
.content-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin: 1rem 0;
    border: 1px solid #e2e8f0;
}

/* Subheaders */
h3 {
    color: #1e293b;
    font-weight: 600;
    margin-top: 1.5rem;
}

/* Text Inputs */
.stTextInput input {
    background-color: #f8fafc !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 0.75rem !important;
    font-size: 0.95rem !important;
    color: #1e293b !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
}

.stTextInput input::placeholder {
    color: #94a3b8 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(14, 165, 233, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #0ea5e9 !important;
}

/* Answer Box */
.answer-box {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-left: 4px solid #0ea5e9;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #1e293b;
    font-size: 1rem;
    line-height: 1.7;
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);
}

/* Source Cards */
.source-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    color: #475569;
    font-size: 0.9rem;
    word-break: break-all;
    transition: all 0.2s ease;
}

.source-card:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;
}

/* Alerts */
.stAlert {
    border-radius: 10px !important;
    border: none !important;
    font-weight: 500 !important;
}

.stSuccess {
    background-color: #d1fae5 !important;
    color: #065f46 !important;
}

.stError {
    background-color: #fee2e2 !important;
    color: #991b1b !important;
}

.stWarning {
    background-color: #fef3c7 !important;
    color: #92400e !important;
}

/* Divider */
hr {
    margin: 2rem 0;
    border: none;
    border-top: 1px solid #e2e8f0;
}

/* Footer */
footer {visibility: hidden;}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
}

::-webkit-scrollbar-thumb {
    background: rgba(14, 165, 233, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(14, 165, 233, 0.7);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown("<div class='main-title'>GoFetch</div>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>⚡ Groq-Powered RAG • Fast • Accurate • Intelligent</p>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("## API Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Used only during this session"
    )

    st.markdown("---")
    st.markdown("### How It Works")
    st.markdown("""
    1. Scrapes news content  
    2. Builds semantic index (FAISS)  
    3. Performs RAG retrieval  
    4. Generates grounded answers  
    """)

if not api_key:
    st.warning("Enter your Groq API key in the sidebar to continue.")
    st.stop()

# ---------------- SESSION INIT ---------------- #
if "ready" not in st.session_state:
    st.session_state.ready = False
    st.session_state.index = None
    st.session_state.chunks = []
    st.session_state.sources = []

# sample urls #
SAMPLE_URLS = [
    "https://www.moneycontrol.com/artificial-intelligence/infosys-exxonmobil-expand-partnership-to-develop-immersion-cooling-for-ai-data-centres-article-13825691.html",
    "https://www.moneycontrol.com/news/india/karnataka-plans-rs-100-crore-multiplex-film-complex-in-bengaluru-under-ppp-13825697.html",
    "https://www.moneycontrol.com/news/business/tata-motors-launches-punch-icng-price-starts-at-rs-7-1-lakh-11098751.html"
]

if "url_inputs" not in st.session_state:
    st.session_state.url_inputs = ["", "", ""]

# ---------------- MAIN CARD ---------------- #
st.markdown("<div class='content-card'>", unsafe_allow_html=True)

st.subheader("Add News Article URLs (Max 3)")

st.markdown("### 🚀 Try Instantly")
st.caption("Click below to auto-fill sample news articles.")

if st.button("📌 Use Sample URLs", key="sample_urls_button"):
    for i in range(3):
        st.session_state[f"url_{i}"] = SAMPLE_URLS[i]
    st.rerun()

urls = []

for i in range(3):
    url = st.text_input(
        f"URL {i+1}",
        key=f"url_{i}"
    )
    urls.append(url)

if st.button("Process Urls", key="process_urls_button"):

    all_chunks = []
    sources = []

    valid_urls = [u.strip() for u in urls if u.strip()]
    if not valid_urls:
        st.error("Please enter at least one valid URL.")
        st.stop()

    with st.spinner("Scraping and indexing articles..."):

        for url in valid_urls:
            text = fetch_text(url)

            if not text.strip():
                continue

            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            sources.extend([url] * len(chunks))

        if all_chunks:
            st.session_state.index = build_faiss(all_chunks)
            st.session_state.chunks = all_chunks
            st.session_state.sources = sources
            st.session_state.ready = True
            st.success("Url Processed")
        else:
            st.error("No readable content found.")

# ---------------- QUESTION SECTION ---------------- #
if st.session_state.ready:

    st.markdown("---")
    st.subheader("Ask a Question")

    query = st.text_input(
        "Type your question here...",
        placeholder="Example: What are the key arguments presented?"
    )

    if query:
        with st.spinner("Generating answer..."):

            answer, srcs = rag_query(
                query,
                st.session_state.chunks,
                st.session_state.sources,
                st.session_state.index,
                api_key
            )

        st.markdown("### Answer")
        st.markdown(
            f"<div class='answer-box'>{answer}</div>",
            unsafe_allow_html=True
        )

        st.markdown("### Sources")
        for s in set(srcs):
            st.markdown(
                f"<div class='source-card'>{s}</div>",
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<hr>
<p style='text-align:center; font-size:0.85rem; color:#64748b; font-weight:500;'>
🚀 Built by Venkata Sai • AI Engineer
</p>
""", unsafe_allow_html=True)
