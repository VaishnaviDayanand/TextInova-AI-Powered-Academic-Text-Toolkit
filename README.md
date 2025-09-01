## **📘 TextInova – AI-Powered Academic Text Toolkit**

An AI-powered toolkit designed to assist students, researchers, and professionals in academic writing. The toolkit includes features for paraphrasing, summarization, and plagiarism detection with support for academic tone.

🚀 Live App: TextInova on Streamlit Cloud  https://textinova.streamlit.app/


---

## **✨ Features & Tech Stack**

## ✍️ Paraphrasing Tool

Model: PegasusForConditionalGeneration (Hugging Face – tuner007/pegasus_paraphrase)

Supports: Normal, Academic Filter, First-person Removal, Active/Passive Voice Conversion


## 📚 Text Summarization

Model: facebook/bart-large-cnn (Hugging Face BART)

Supports: Abstractive & Extractive summarization with tone (neutral, formal, informal) and length control (short, medium, long, custom)


## 🔎 Plagiarism Detection

AI Authorship Detection

Model: Hello-SimpleAI/chatgpt-detector-roberta

Detects probability of AI vs Human-written content


Intrinsic Plagiarism (Self-similarity)

Technique: TfidfVectorizer + Cosine Similarity (scikit-learn)

Detects repeated patterns & similarity within the text



## **📂 File Support**

Libraries: python-docx, PyPDF2, pdfplumber, PyMuPDF, pdf2image + pytesseract (OCR for scanned PDFs)

Upload & process .pdf, .docx, and .txt


## **🎨 Custom UI**

Framework: Streamlit

Styling: Custom CSS for backgrounds, colors, and highlighted outputs




---

## **👥 Developers**

Vaishnavi D

G S Priya

Sudeep Kumar G

Preetham K



---

## **📝 Disclaimer**

This app is a prototype for academic assistance and does not guarantee 100% accuracy. Always review generated outputs critically.


---