import streamlit as st
from PIL import Image
from backend.utils import extract_text_from_file
from backend.plagiarism_detection import run_plagiarism_detection
import re

# Streamlit Page Settings
st.set_page_config(page_title="Academic Writing Assistant", layout="wide")

# Logo and Title
col1, col2 = st.columns([1, 8])
with col1:
    logo = Image.open("assets/logo.png")  # optional: place a logo
    st.image(logo, width=70)
with col2:
    st.title("Academic Writing Assistant")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Paraphrasing", "Text Summarization", "Plagiarism Detection"])

# Routing Pages
if page == "Home":
    st.header("Welcome! 🎯")
    st.markdown("""
        This tool assists in academic writing through:
        - ✍️ **Paraphrasing**
        - 📚 **Text Summarization**
        - 🔎 **Plagiarism Detection**

        Navigate through the sidebar to use features!
    """)

elif page == "Paraphrasing":
    st.header("Paraphrasing Tool ✍️")
    input_text = st.text_area("Enter text to paraphrase:", height=300)
    if st.button("Paraphrase"):
        if input_text.strip() != "":
            with st.spinner("Paraphrasing..."):
                # Placeholder output
                st.success("Here is the paraphrased text (coming soon).")
        else:
            st.warning("Please enter some text!")

elif page == "Text Summarization":
    st.header("Text Summarization Tool 📚")
    input_text = st.text_area("Enter text to summarize:", height=300)
    if st.button("Summarize"):
        if input_text.strip() != "":
            with st.spinner("Summarizing..."):
                # Placeholder output
                st.success("Here is the summarized text (coming soon).")
        else:
            st.warning("Please enter some text!")

elif page == "Plagiarism Detection":
    st.header("Plagiarism Detection Tool 🔎")

    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
    input_text = st.text_area("Or paste your text here:", height=300)

    final_text = ""
    if uploaded_file:
        final_text = extract_text_from_file(uploaded_file)
    elif input_text.strip():
        final_text = input_text

    if st.button("Check for Plagiarism") and final_text:
        with st.spinner("Analyzing..."):
            result = run_plagiarism_detection(final_text)
            st.success(f"Plagiarism Score: {result['score']}%")

            st.subheader("🔍 Highlighted Text with Annotations:")

            extrinsic = set(result['extrinsic'])
            intrinsic = set(result['intrinsic'])

            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(final_text)

            def highlight_text(sentences, extrinsic, intrinsic):
                highlighted = ""
                for s in sentences:
                    escaped = re.escape(s)
                    if s in extrinsic:
                        highlighted += f'<span style="background-color:#ffcccc;">{s}</span> '
                    elif s in intrinsic:
                        highlighted += f'<span style="background-color:#fff3cd;">{s}</span> '
                    else:
                        highlighted += s + " "
                return highlighted

            html_result = highlight_text(sentences, extrinsic, intrinsic)
            st.markdown(html_result, unsafe_allow_html=True)

            st.markdown("""
            **Legend**  
            🔴 <span style="background-color:#ffcccc;">Red</span>: Detected from online sources (extrinsic)  
            🟠 <span style="background-color:#fff3cd;">Yellow</span>: Writing style anomaly (intrinsic)
            """, unsafe_allow_html=True)