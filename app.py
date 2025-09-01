import streamlit as st
import base64
import os
from backend.utils import read_pdf, read_docx, read_txt
from backend.plagiarism_detection import AI_detector
from backend.intrinsic_detector import intrinsic_plagiarism_score
from backend.summarizer import summarize
from backend.paraphraser import paraphrase_text

# Convert image to base64 string
def image_to_base64(image_path):
    """Convert image to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set background image for the app and apply white text styling
def set_background(image_path):
    """Set the background image for the Streamlit app."""
    if os.path.exists(image_path):
        encoded_image = image_to_base64(image_path)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                height: 100vh;
                color: white;
            }}

            /* Mobile fix */
            @media (max-width: 768px) {{
                .stApp {{
                    background-size: contain !important;
                    background-attachment: scroll !important;
                    background-repeat: no-repeat !important;
                    background-position: top center !important;
                }}
            }}

            /* Radio buttons yellow */
            .stRadio > div[role="radiogroup"] label {{
                color: yellow !important;
                font-weight: bold;
            }}

            /* Spinner (loading circle) yellow */
            .stSpinner > div {{
                border-top-color: yellow !important;
            }}

            /* File name yellow */
            .uploadedFileName {{
                color: yellow !important;
                font-weight: bold;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write(f"Image not found at {image_path}. Please check the path.")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Paraphrasing", "Text Summarization", "Plagiarism Detection", "About"])

# Routing Pages
if page == "Home":
    set_background("assets/home.png")

elif page == "Paraphrasing":
    set_background("assets/paraphraser.png")
    st.header("Paraphrasing Tool ✍️")

    text = st.text_area("Enter text to paraphrase:")

    option = st.selectbox(
        "Choose paraphrasing style:",
        ("Normal", "Academic Filter", "First Person Removal", "Active/Passive Voice Change")
    )

    voice_type = "passive"
    if option == "Active/Passive Voice Change":
        voice_type = st.radio("Choose voice conversion:", ("Passive", "Active"))

    if st.button("Paraphrase"):
        if text:
            with st.spinner("Paraphrasing..."):
                option_map = {
                    "Normal": "normal",
                    "Academic Filter": "academic_filter",
                    "First Person Removal": "first_person_removal",
                    "Active/Passive Voice Change": "active_passive"
                }
                selected_option = option_map[option]
                result = paraphrase_text(text, option=selected_option, voice_type=voice_type)
            st.success("Paraphrased Text:")
            st.write(result)
        else:
            st.warning("Please enter some text.")

elif page == "Text Summarization":
    set_background("assets/summarization.png")
    st.header("Text Summarization Tool 📚")
    
    input_text = st.text_area("Enter text to summarize:", height=300)

    st.subheader("📊 Summarization Settings")
    summary_type = st.selectbox("Choose summary type:", ["abstractive", "extractive"])
    tone = st.selectbox("Choose tone:", ["neutral", "formal", "informal"])
    length_option = st.selectbox("Choose summary length:", ["short", "medium", "long", "custom"])

    custom_min = custom_max = None
    if length_option == "custom":
        custom_min = st.number_input("Enter custom min length:", min_value=10, max_value=1000, value=50)
        custom_max = st.number_input("Enter custom max length:", min_value=10, max_value=2000, value=150)

    if st.button("Summarize"):
        if input_text.strip() != "":
            with st.spinner("Summarizing..."):
                try:
                    if summary_type == "extractive":
                        summary = summarize(input_text)
                    else:
                        if length_option == "custom":
                            summary = summarize(
                                input_text,
                                summary_type=summary_type,
                                tone=tone,
                                length=length_option,
                                custom_length_range=(custom_min, custom_max)
                            )
                        else:
                            summary = summarize(
                                input_text,
                                summary_type=summary_type,
                                tone=tone,
                                length=length_option
                            )
                    st.subheader("🔹 Summary:")
                    st.success("Summary generated successfully! ✅")
                    st.markdown(
                        f"""
                        <div style="background-color: #ffd700; padding: 15px; border-radius: 10px; color: black; font-weight: bold;">
                            🔹 Summary:<br><br>{summary}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter some text!")

elif page == "Plagiarism Detection":
    set_background("assets/plagiarism.png")
    st.header("Plagiarism Detection Tool 🔍")

    uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    # Display filename in yellow if uploaded
    if uploaded_file is not None:
        st.markdown(
            f"<p style='color:yellow; font-weight:bold;'>📂 Selected File: {uploaded_file.name}</p>",
            unsafe_allow_html=True
        )

    input_text = st.text_area("Or paste your text here:", height=300, key="plag_text_area")

    final_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            final_text = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            final_text = read_docx(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            final_text = read_txt(uploaded_file)
        else:
            st.warning("Unsupported file type!")
    elif input_text.strip() != "":
        final_text = input_text

    if st.button("Check for Integrity") and final_text:
        with st.spinner("Analyzing..."):
            ai_result = AI_detector(final_text)
            intrinsic_result = intrinsic_plagiarism_score(final_text)

            st.subheader("AI Authorship Detection 🤖🧑‍💻")
            st.write(f"**Human Probability:** {ai_result['Human Probability']}%")
            st.write(f"**AI Probability:** {ai_result['AI Probability']}%")

            st.subheader("Intrinsic Similarity Detection 🔄")
            st.write(f"**Average Similarity Score:** {intrinsic_result['similarity_score']}%")

            if intrinsic_result['similar_pairs']:
                st.write("### Highly Similar Sentence Pairs:")
                for pair in intrinsic_result['similar_pairs']:
                    st.markdown(
                        f"""
                         <div style="background-color:#fff3cd; color:black; padding:15px; border-radius:10px; border:1px solid #ffeeba;">
                            <strong>1️⃣ {pair['sentence_1']}</strong><br><br>
                            <strong>2️⃣ {pair['sentence_2']}</strong><br><br>
                            <em>Similarity: {pair['similarity']}</em>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.success("No significant self-plagiarism detected!")

    st.markdown("""  
    - 🤖 **AI Authorship Detection**: Detects if the text is likely AI-generated.  
    - 🔄 **Intrinsic Similarity Detection**: Checks for repeated patterns within your document.
    """)

elif page == "About":
    set_background("assets/about.png")
    st.header("About the Toolkit 📘")
    st.markdown("""
    ### 🛠 **Academic Writing Assistant**

    This tool is designed to assist students, researchers, and professionals in producing high-quality academic content. Key features include:

    - ✍️ **Paraphrasing Tool:** Helps rewrite sentences while maintaining the original meaning and in academic tone.
    - 📚 **Text Summarization:** Condenses long documents into clear summaries, with tone and length customization.
    - 🔎 **Academic Integrity Checker:** Detects AI-generated content and checks for intrinsic plagiarism within your text.

    #### 👥 **Developers:**
    - Vaishnavi D
    - G S Priya
    - Sudeep Kumar G
    - Preetham K

    #### 📝 **Disclaimer:**
    This app is a prototype for academic assistance and **does not guarantee 100% accuracy.** Always review generated outputs critically.

    ---
    **Tech Stack:** Streamlit, Hugging Face Transformers, Python  
    """, unsafe_allow_html=True)