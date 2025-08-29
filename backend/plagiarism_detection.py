from .utils import read_pdf, read_docx, read_txt
from .intrinsic_detector import intrinsic_plagiarism_score
from .AI_detector import detect_ai_text

# Export AI_detector for external use
AI_detector = detect_ai_text
# Export intrinsic_detector for external use
intrinsic_detector = intrinsic_plagiarism_score

def process_file(uploaded_file):
    """
    Reads and extracts text based on file type.
    """
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'pdf':
        text = read_pdf(uploaded_file)
    elif file_type == 'docx':
        text = read_docx(uploaded_file)
    elif file_type == 'txt':
        text = read_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type")

    return text


def check_ai_generated(text):
    return detect_ai_text(text)


def check_intrinsic_plagiarism(text):
    return intrinsic_plagiarism_score(text)
