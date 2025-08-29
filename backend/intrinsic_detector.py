from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def intrinsic_plagiarism_score(text):
    sentences = [s for s in text.split('\n') if len(s.strip()) > 20] # filter short lines
    if len(sentences) < 2:
        return {
            "similarity_score": 0,
            "similar_pairs": []
        }
    vectorizer = TfidfVectorizer().fit_transform(sentences)
    similarity_matrix = cosine_similarity(vectorizer)

    similar_pairs = []
    n = len(sentences)
    total_similarity = 0
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_matrix[i, j]
            if sim > 0.7: # You can tweak this threshold
                similar_pairs.append({
                    "sentence_1": sentences[i],
                    "sentence_2": sentences[j],
                    "similarity": round(sim, 2)
                })
            total_similarity += sim
            count += 1

    avg_similarity = (total_similarity / count) * 100 if count > 0 else 0

    return {
        "similarity_score": round(avg_similarity, 2),
        "similar_pairs
