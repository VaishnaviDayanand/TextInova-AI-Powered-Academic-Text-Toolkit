📚 TextInova - AI-powered Academic Text Toolkit

🚀 TextInova is an AI-powered academic assistant that helps students, educators, and researchers with:

✨ Paraphrasing (with Academic English filter option)

📝 Text Summarization (extractive + abstractive, with word/length & tone options)

🔍 Plagiarism Detection (AI-based + intrinsic detection using stylometry)

🌟 Features

✅ Paraphrasing

Rewrites text while maintaining meaning.

Includes an Academic English filter for formal writing.

✅ Text Summarization

Provides both extractive and abstractive summaries.

Option to set tone (formal, casual, etc.).

Control summary length by number of words/sentences.

✅ Plagiarism Detection

AI-based detection (checks against AI-generated content).

Intrinsic plagiarism detection (stylometry ML-based, checks inconsistencies within text).

Displays plagiarism percentage for uploaded files (PDF/DOC/TXT).

🏗️ Project Structure
textinova/
│── app.py                 # Main Streamlit app
│── requirements.txt       # Dependencies for Streamlit Cloud
│── README.md              # Project documentation
│── assets/                # Logos, icons, images
│── backend/
│   ├── utils.py           # File reading & helpers
│   ├── paraphrase.py      # Paraphrasing logic
│   ├── summarizer.py      # Summarization logic
│   ├── plagiarism_ai.py   # AI plagiarism detection
│   ├── plagiarism_intrinsic.py # Intrinsic detection

⚙️ Installation (Local Setup)

Clone the repository:

git clone https://github.com/<your-username>/textinova-ai-powered-academic-text-toolkit.git
cd textinova-ai-powered-academic-text-toolkit


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py

☁️ Deployment on Streamlit Cloud

Push your code to GitHub with:

app.py at the root

requirements.txt at the root

README.md at the root

Go to Streamlit Cloud
.

Create a new app → connect your GitHub repo → select branch and app.py.

Deploy 🎉

📊 Tech Stack

Python 3.9+

Streamlit (frontend & UI)

Transformers (Facebook BART, Pegasus, etc.) for summarization

PyTorch for model execution

scikit-learn + stylometry ML models for intrinsic plagiarism

PyPDF2 / python-docx for file handling

🧑‍🤝‍🧑 Contributors

👩‍💻 Developers:

Vaishnavi Dayanand

📌 Future Enhancements

🌐 Add support for multi-language paraphrasing & summarization.

📑 Integration with reference managers (Zotero, Mendeley).

⚡ Improve plagiarism detection using hybrid semantic models.

📜 License

This project is licensed under the MIT License – free to use, modify, and distribute.