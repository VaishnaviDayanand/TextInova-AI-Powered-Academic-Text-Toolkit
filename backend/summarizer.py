import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import nltk
import re
import fitz  # python -m pip install pymupdf
from pdf2image import convert_from_path
import pytesseract

# Download NLTK tokenizer (only first time)
nltk.data.path.clear()
nltk.download('punkt')

# Load BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# ------------------------
# Extractive summarizer
# ------------------------
def extractive_summarize(text, num_sentences=2):
    """
    Simple extractive summarizer: picks the longest sentences.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    ranked = sorted(sentences, key=lambda s: len(s), reverse=True)
    selected = ranked[:num_sentences]
    return ' '.join(selected)

# ------------------------
# Tone changer
# ------------------------
def change_tone(text, tone):
    """
    Adjust tone: neutral, formal, or informal.
    """
    if tone == 'informal':
        replacements = {
            "do not": "don't",
            "cannot": "can't",
            "will not": "won't",
            "is not": "isn't"
        }
    elif tone == 'formal':
        replacements = {
            "don't": "do not",
            "can't": "cannot",
            "won't": "will not",
            "isn't": "is not"
        }
    else:
        replacements = {}

    for k, v in replacements.items():
        text = re.sub(r'\b' + re.escape(k) + r'\b', v, text, flags=re.IGNORECASE)
    return text

# ------------------------
# Clean up unwanted phrases
# ------------------------
def clean_summary(text):
    """
    Removes unwanted marketing/website-related phrases and currency references.
    """
    text = re.sub(r'http\S+|www\S+|\bvisit\b.*|call.*|click here.*|Back to.*|Follow us.*|For confidential.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\(US\$?.*?\)|£[\d\.]+|priced.*?copies?', '', text)
    text = re.sub(r'\bsamaritans\b.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
    return text.strip()

# ------------------------
# Summarize main function
# ------------------------
def summarize(text, summary_type='abstractive', tone='neutral', length='medium',
              num_sentences_custom=None, custom_length_range=None):
    """
    Handles both abstractive & extractive summarization with tone & length customization.
    """
    if summary_type == 'extractive':
        # Decide number of sentences
        num_sentences_map = {'short': 2, 'medium': 5, 'long': 10}
        num_sentences = num_sentences_custom if num_sentences_custom is not None else num_sentences_map.get(length, 3)
        summary = extractive_summarize(text, num_sentences)
    else:
        # Define length ranges
        if custom_length_range is not None:
            min_len, max_len = custom_length_range
        else:
            length_map = {
                'short': (50, 100),
                'medium': (100, 300),
                'long': (300, 500)
            }
            min_len, max_len = length_map.get(length, (80, 120))

        # Tokenize & generate abstractive summary
        inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True).to(device)
        summary_ids = model.generate(
            inputs["input_ids"],
            min_length=min_len,
            max_length=max_len,
            num_beams=10,
            length_penalty=1,
            early_stopping=True,
            no_repeat_ngram_size=0
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary = clean_summary(summary)

    # Apply tone change
    return change_tone(summary, tone)

# ------------------------
# Read PDF using PyMuPDF
# ------------------------
def read_pdf(file_path):
    """
    Extract text from a PDF using PyMuPDF.
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

# ------------------------
# OCR fallback for scanned PDFs
# ------------------------
def read_pdf_with_ocr(file_path):
    """
    Extract text from scanned PDFs using OCR (Tesseract).
    """
    images = convert_from_path(file_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

# ------------------------
# CLI interaction
# ------------------------
def get_user_input():
    """
    Interactive CLI for user input.
    """
    mode = input("Do you want to summarize (1) Text or (2) PDF? Enter 1 or 2: ").strip()

    if mode == "1":
        input_text = input("Enter the text to summarize:\n")
    elif mode == "2":
        pdf_path = input("Enter the path to your PDF file: ").strip()
        text = read_pdf(pdf_path)
        if not text.strip():
            print("No text found. Attempting OCR on the PDF.")
            text = read_pdf_with_ocr(pdf_path)
        input_text = text
    else:
        raise ValueError("Invalid input. Please enter 1 or 2.")

    summary_type = input("Choose summary type (abstractive / extractive): ").strip().lower()
    tone = input("Choose tone (neutral / formal / informal): ").strip().lower()

    custom_length_range = None
    use_predefined = input("Do you want to choose from predefined lengths (short / medium / long)? (yes/no): ").strip().lower()

    if use_predefined == "yes":
        length = input("Choose length (short / medium / long): ").strip().lower()
    else:
        length = "custom"
        min_len = int(input("Enter custom min length: "))
        max_len = int(input("Enter custom max length: "))
        custom_length_range = (min_len, max_len)

    return input_text, summary_type, tone, length, custom_length_range

# ------------------------
# Run as script
# ------------------------
if __name__ == "__main__":
    input_text, summary_type, tone, length, custom_length_range = get_user_input()

    summary = summarize(
        input_text,
        summary_type=summary_type,
        tone=tone,
        length=length,
        custom_length_range=custom_length_range
    )

    print("\n🔹 Summary:\n", summary)