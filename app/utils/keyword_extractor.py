import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordExtractor:
    """
    Keyword Extraction using TF-IDF (single text)
    """

    def __init__(self, max_features=100, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range

    def extract(self, text: str, top_n: int = 5):
        """
        Extract top keywords from input text
        """

        # Safety check
        if not text or not isinstance(text, str):
            return []

        try:
            # Initialize vectorizer
            vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=self.max_features,
                ngram_range=self.ngram_range,
            )

            # Fit on single text
            tfidf_matrix = vectorizer.fit_transform([text])

            # Get feature names
            feature_names = np.array(vectorizer.get_feature_names_out())

            # Get TF-IDF scores
            scores = tfidf_matrix.toarray()[0]

            # Remove zero-score words
            valid_indices = np.where(scores > 0)[0]

            if len(valid_indices) == 0:
                return []

            # Sort by importance
            sorted_indices = valid_indices[np.argsort(scores[valid_indices])[::-1]]

            # Select top N keywords
            top_indices = sorted_indices[:top_n]

            keywords = feature_names[top_indices]

            return keywords.tolist()

        except Exception as e:
            print(f"[KeywordExtractor Error]: {e}")
            return []