import streamlit as st
from rag_utils import fetch_text, chunk_text, build_faiss, rag_query
from dotenv import load_dotenv
st.set_page_config(
    page_title="AI Q&A Chat",
    page_icon="🤖",
    layout="centered"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');

.page-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700; /* Bold */
  font-size: 3rem;  /* Adjust size as needed */
  color: #FFFFFF;   /* White text for contrast */
  text-align: center;
  letter-spacing: 1px; /* Slight spacing for clarity */
}

.fading-list {
  -webkit-mask-image: linear-gradient(to bottom, black 80%, rgba(0, 0, 0, 0));
  mask-image: linear-gradient(to bottom, black 80%, rgba(0, 0, 0, 0));
}

/* Add a subtle border to the sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid #22252B;
}

/* Style inputs to match the dark theme */
.stTextInput > div > div > input {
    background-color: #FAFAFA !important;
    color: #000000 !important;
    border: 0.8px solid #2E3138 !important;
}

div[data-baseweb="input"],
div[data-baseweb="base-input"],
input,
textarea {
  color: black !important;
  background-color: #FAFAFA !important;
}

/* Main container styling */
.main .block-container {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin-top: 1rem;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #635BFF, #7C3AED) !important;
    color: white !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 0.5rem 2rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(99, 91, 255, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 91, 255, 0.4) !important;
}

/* Text input styling */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 2px solid #e1e5e9 !important;
    padding: 0.75rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #635BFF !important;
    box-shadow: 0 0 0 3px rgba(99, 91, 255, 0.1) !important;
}

/* Info box styling */
.stAlert {
    border-radius: 10px !important;
    border-left: 4px solid #635BFF !important;
}
</style>
<h1 class="page-title">GoFetch</h1>
<p style='text-align: center; color: gray;'>
 Groq LLM • Fast • Accurate • Lightweight
</p>
<hr>
""", unsafe_allow_html=True)
load_dotenv()

with st.sidebar:
    st.header("About")
    st.write("""
    This application uses **Groq LLM APIs** to answer
    technical and conceptual questions with low latency.
    """)

st.title(" GoFetch – News Research Tool")
st.write("🔍 Retrieved sources for this question:")



if "ready" not in st.session_state:
    st.session_state.ready = False

urls = [st.text_input(f"URL {i+1}") for i in range(3)]

if st.button("Process URLs"):
    all_chunks = []
    sources = []
    
    valid_urls = [url.strip() for url in urls if url.strip()]
    st.info(f"Processing {len(valid_urls)} URLs...")

    for i, url in enumerate(valid_urls):
        try:
            st.write(f"Processing URL {i+1}: {url}")
            
            text = fetch_text(url)
            st.write(f"Extracted {len(text)} characters from URL {i+1}")


            if not text.strip():
                st.warning(f"Skipped (no readable content): {url}")
                continue
        
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            sources.extend([url] * len(chunks))
            st.success(f"✅ Processed {len(chunks)} chunks from URL {i+1}")
            
        except Exception as e:
            st.error(f"❌ Error processing URL {i+1}: {str(e)}")
            continue

    if all_chunks:
        st.session_state.index = build_faiss(all_chunks)
        st.session_state.chunks = all_chunks
        st.session_state.sources = sources
        st.session_state.ready = True
        st.success(f"✅ Knowledge base ready with {len(all_chunks)} total chunks from {len(set(sources))} URLs!")
    else:
        st.error("No valid content found from any URLs.")

if st.session_state.ready:
    with st.container():
        st.subheader("Ask a Question")
        query = st.text_input(
            "Enter your question",
            placeholder="e.g., Why are liquid cooling systems gaining popularity?"
        )

    if query:
        with st.spinner("Generating answer..."):
            answer, srcs = rag_query(
                query,
                st.session_state.chunks,
                st.session_state.sources,
                st.session_state.index
            )

        st.markdown("### ✅ Answer")
        st.info(answer)

        st.markdown("<div class='fading-list'>", unsafe_allow_html=True)
        st.subheader("Sources")
        for s in set(srcs):
            st.write(s)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""<hr><p style='text-align: center; font-size: 12px; color: gray;'>
Built by Venkata Sai • AI & Full Stack Enthusiast
</p>
""", unsafe_allow_html=True)