# backend/intrinsic_detector.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def check_intrinsic_plagiarism(text, reference_texts):
    """
    Checks for intrinsic plagiarism by comparing the text to reference texts using cosine similarity.
    :param text: The text to check for plagiarism
    :param reference_texts: List of reference texts to compare against
    :return: Boolean indicating if plagiarism is detected
    """
    # Combine the text with reference texts
    all_texts = reference_texts + [text]
    
    # Convert the texts into TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate cosine similarity between the last vector (the text) and all reference texts
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # If any cosine similarity is above a threshold (e.g., 0.8), consider it plagiarism
    if max(cosine_similarities[0]) > 0.8:
        return True
    return False