# backend/plagiarism_detector.py
from .intrinsic_detector import check_intrinsic_plagiarism
from .extrinsic_detector import check_extrinsic_plagiarism

def run_plagiarism_detection(text, reference_texts):
    """
    Runs both intrinsic and extrinsic plagiarism checks.
    :param text: The text to check for plagiarism
    :param reference_texts: List of reference texts to compare against (for intrinsic check)
    :return: Boolean indicating if plagiarism is detected
    """
    # Run intrinsic plagiarism check
    intrinsic_plagiarism = check_intrinsic_plagiarism(text, reference_texts)
    
    # Run extrinsic plagiarism check
    extrinsic_plagiarism = check_extrinsic_plagiarism(text)
    
    # If either intrinsic or extrinsic plagiarism is detected, return True
    return intrinsic_plagiarism or extrinsic_plagiarism