# momoru/core/scanner.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from momoru.config import CONFIG  # 🌟 Ganti ConfigManager dengan objek global CONFIG baru

class BuzzerScanner:
    def __init__(self, comments: list[str], target_user: str, threshold: float = 0.75):
        self.comments = comments
        self.target_user = target_user
        self.threshold = threshold
        
        # 🌟 Ambil template langsung dari dictionary CONFIG global bawaan config.yaml
        self.templates = CONFIG["intelligence"].get("templates", [])

    def calculate_similarity(self) -> float:
        if not self.comments or not self.templates:
            return 0.0
        
        # Vectorize menggunakan TF-IDF Matrix
        vectorizer = TfidfVectorizer().fit_transform(self.templates + self.comments)
        vectors = vectorizer.toarray()
        
        num_templates = len(self.templates)
        similarity_matrix = cosine_similarity(vectors[num_templates:], vectors[:num_templates])
        
        return float(np.max(similarity_matrix)) if similarity_matrix.size > 0 else 0.0