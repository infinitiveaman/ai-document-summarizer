import streamlit as st
from transformers import pipeline
import fitz
import tempfile

summarizer = pipeline("summarization", model="t5-small")

st.set_page_config(page_title="AI Document Summarizer", page_icon="📄", layout="wide")

st.markdown("""
    <style>
        .header {
            background-color: #0078D7;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
        }
        .separator {
            border-bottom: 4px solid #4CAF50;
            margin: 20px 0;
        }
        .main-container {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
        }
        .footer {
            background-color: #222;
            color: white;
            text-align: center;
            padding: 15px;
            margin-top: 20px;
            border-radius: 10px;
        }
        .footer a {
            color: #FFD700;
            font-weight: bold;
            text-decoration: none;
            margin: 0 10px;
        }
        .summary-box {
            background-color: #FFF9C4;  /* Light Yellow */
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #0078D7;
            color: #1A237E; /* Dark Blue */
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <h1> Document Summarizer</h1>
        <h4> Built by <a href="https://www.linkedin.com/in/infinitiveaman/" target="_blank" style="color: yellow;">Aman Yadav</a></h4>
        <p>🔗 <a href="https://github.com/infinitiveaman" target="_blank" style="color: white;">GitHub</a> | ✉️ <a href="mailto:infinitiveaman@gmail.com" style="color: white;">Email</a></p>
    </div>
    <div class="separator"></div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.write("📤 Upload a **PDF document**, and I will generate a **short and meaningful summary** for you.")

uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name  

    doc = fitz.open(temp_pdf_path)  
    text = ""
    for page in doc:
        text += page.get_text()

    return text

def split_text(text, chunk_size=900, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

if uploaded_file is not None:
    with st.spinner("⏳ Extracting text from PDF... Please wait..."):
        text = extract_text_from_pdf(uploaded_file)

    st.subheader("📊 Document Stats:")
    st.write(f"**Total Words:** {len(text.split())}")

    if len(text) > 0:
        text_chunks = split_text(text)
        summaries = []
        progress_bar = st.progress(0)

        for i, chunk in enumerate(text_chunks):
            try:
                summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                st.error(f"Error summarizing chunk: {str(e)}")
                break
            progress_bar.progress((i + 1) / len(text_chunks))

        final_summary = " ".join(summaries)

        st.subheader("📃 Summary:")
        st.markdown(f'<div class="summary-box">{final_summary}</div>', unsafe_allow_html=True)

        st.download_button("📥 Download Summary", final_summary, "summary.txt", "text/plain")

    else:
        st.error("⚠️ Could not extract text from the PDF. Try another file.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <p> <a href="https://github.com/infinitiveaman" target="_blank">GitHub</a> | 
         <a href="https://www.linkedin.com/in/infinitiveaman/" target="_blank">LinkedIn</a> | 
         <a href="mailto:infinitiveaman@gmail.com">Email</a></p>
        <p> Aman Yadav </p>
    </div>
""", unsafe_allow_html=True)
