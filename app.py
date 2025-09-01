import streamlit as st
import base64
import os
from backend.utils import read_pdf, read_docx, read_txt
from backend.plagiarism_detection import AI_detector
from backend.plagiarism_detection import intrinsic_detector
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
        # Convert the image to base64
        encoded_image = image_to_base64(image_path)
        
        # Create the background style using base64 image data and add text color white
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                height: 100vh; /* Ensure the background covers the entire screen */
                color: white; /* Make all text white */
            }}

            /* Ensure white color for text input and selectbox labels */
            .stTextInput, .stTextArea, .stSelectbox, .stSlider, .stNumberInput {{
                color: white; /* Text inside input fields */
            }}

            .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stNumberInput label {{
                color: white; /* Labels of text inputs and other widgets */
            }}

            .stButton, .stCheckbox, .stRadio label {{
                color: white; /* Button and checkbox labels */
            }}

            /* Change button text color to yellow */
            .stButton button {{
                color: yellow; /* Set button text color to yellow */
                background-color: transparent; /* Transparent background to preserve the original button styling */
                border: 1px solid yellow; /* Optional: Adds a yellow border to the button */
            }}

            /* Make the header white */
            .css-1d391kg {{
                color: white; /* Headers with white font color */
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

    # Add option selector for paraphrasing type
    option = st.selectbox(
        "Choose paraphrasing style:",
        ("Normal", "Academic Filter", "First Person Removal", "Active/Passive Voice Change")
    )

    # If Active/Passive Voice Change is selected, let user choose which voice
    voice_type = "passive" # default
    if option == "Active/Passive Voice Change":
        voice_type = st.radio("Choose voice conversion:", ("Passive", "Active"))

    if st.button("Paraphrase"):
        if text:
            with st.spinner("Paraphrasing..."):
                # Map UI option to function option values
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

    # Filter options
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

    # Custom CSS for uploader styling
    st.markdown(
        """
        <style>
        /* Label above the uploader */
        .stFileUploader label {
            color: white !important;
            font-weight: bold;
        }

        /* Upload button container (Browse files) */
        .stFileUploader div[role="button"] {
            color: black !important;               /* Text color */
            background-color: #f0f0f0 !important;  /* Light background */
            border: 1px solid #ccc;
            border-radius: 5px;
            font-weight: bold;
        }

        /* Make sure the icon inside uploader is also black */
        .stFileUploader div[role="button"] svg {
            fill: black !important;
        }

        /* On hover for upload button */
        .stFileUploader div[role="button"]:hover {
            background-color: #ddd !important;
            color: black !important;
        }

        /* Uploaded file name text */
        .uploadedFileName {
            color: yellow !important;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload a file (PDF, DOCX, or TXT)", 
        type=["pdf", "docx", "txt"],
        label_visibility="visible"
    )
    input_text = st.text_area("Or paste your text here:", height=300, key="plag_text_area")

    final_text = ""

    # Only process the uploaded file if it exists
    if uploaded_file is not None:
        # Inject JS+CSS to highlight uploaded file name
        st.markdown(
            """
            <script>
            setTimeout(() => {
                let els = window.parent.document.querySelectorAll('span');
                els.forEach(el => {
                    if (el.innerText.includes('.pdf') || el.innerText.includes('.docx') || el.innerText.includes('.txt')) {
                        el.style.color = 'yellow';
                        el.style.fontWeight = 'bold';
                    }
                });
            }, 100);
            </script>
            """,
            unsafe_allow_html=True
        )

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
            # 1️⃣ AI Detection
            ai_result = AI_detector(final_text)
            # 2️⃣ Intrinsic Plagiarism Check
            intrinsic_result = intrinsic_detector(final_text)

            # AI Authorship Results
            st.subheader("AI Authorship Detection 🤖🧑‍💻")
            st.write(f"**Human Probability:** {ai_result['Human Probability']}%")
            st.write(f"**AI Probability:** {ai_result['AI Probability']}%")

            # Intrinsic Similarity Results
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

    # Legend (Optional)
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