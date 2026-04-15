import joblib
import numpy as np

from app.utils.text_cleaner import clean_text
from app.utils.keyword_extractor import KeywordExtractor


class PredictionService:
    def __init__(self):
        """
        Load model and vectorizer once
        """
        self.model = joblib.load("app/models/sentiment_model.pkl")
        self.vectorizer = joblib.load("app/models/tfidf_vectorizer.pkl")

        self.keyword_extractor = KeywordExtractor()

        # Label mapping
        self.label_map = {
            0: "negative",
            1: "neutral",
            2: "positive"
        }

    def predict(self, text: str):
        """
        Full prediction pipeline
        """

        # -------- 1. Input validation --------
        if not text or not isinstance(text, str):
            return {
                "error": "Invalid input text"
            }

        # -------- 2. Clean text --------
        cleaned_text = clean_text(text)

        # -------- 3. Transform text --------
        text_vector = self.vectorizer.transform([cleaned_text])

        # -------- 4. Predict sentiment --------
        prediction = self.model.predict(text_vector)[0]

        # -------- 5. Confidence score --------
        try:
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(text_vector)
                confidence = float(np.max(probs))
            else:
                confidence = None
        except:
            confidence = None

        # -------- 6. Convert label --------
        sentiment = self.label_map.get(prediction, "unknown")

        # -------- 7. Extract keywords --------
        keywords = self.keyword_extractor.extract(cleaned_text)

        # -------- 8. Build response --------
        result = {
            "input_text": text,
            "cleaned_text": cleaned_text,
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": keywords
        }

        return result