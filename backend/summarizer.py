import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import nltk
import re
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path

# Download NLTK tokenizer (first run only)
nltk.download('punkt', quiet=True)

# Load BART model & tokenizer
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
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    ranked = sorted(sentences, key=lambda s: len(s), reverse=True)
    return ' '.join(ranked[:num_sentences])


# ------------------------
# Tone changer
# ------------------------
def change_tone(text, tone):
    if tone == 'informal':
        replacements = {"do not": "don't", "cannot": "can't", "will not": "won't", "is not": "isn't"}
    elif tone == 'formal':
        replacements = {"don't": "do not", "can't": "cannot", "won't": "will not", "isn't": "is not"}
    else:
        replacements = {}

    for k, v in replacements.items():
        text = re.sub(r'\b' + re.escape(k) + r'\b', v, text, flags=re.IGNORECASE)
    return text


# ------------------------
# Clean summary text
# ------------------------
def clean_summary(text):
    text = re.sub(r'http\S+|www\S+|\bvisit\b.*|call.*|click here.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ------------------------
# Main summarizer function
# ------------------------
def summarize(text, summary_type='abstractive', tone='neutral', length='medium',
              num_sentences_custom=None, custom_length_range=None):

    if summary_type == 'extractive':
        num_sentences_map = {'short': 2, 'medium': 5, 'long': 10}
        num_sentences = num_sentences_custom or num_sentences_map.get(length, 3)
        summary = extractive_summarize(text, num_sentences)

    else:
        length_map = {'short': (50, 100), 'medium': (100, 300), 'long': (300, 500)}
        min_len, max_len = custom_length_range or length_map.get(length, (80, 120))

        inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True).to(device)
        summary_ids = model.generate(inputs["input_ids"], min_length=min_len, max_length=max_len,
                                     num_beams=10, length_penalty=1, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary = clean_summary(summary)

    return change_tone(summary, tone)


# ------------------------
# PDF reading utilities
# ------------------------
def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text


def read_pdf_with_ocr(file_path):
    images = convert_from_path(file_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text