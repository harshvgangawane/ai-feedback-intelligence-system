# app/services/insight_service.py


class InsightService:
    def __init__(self):
        pass

    def generate_insight(self, sentiment: str, keywords: list, domain=None, category=None, product=None):
        """
        Generate business-friendly insight from prediction
        """

        # Safety
        if not sentiment:
            return "No insight available."

        # Format keywords
        keyword_text = ", ".join(keywords) if keywords else "general feedback"

        # -------- POSITIVE --------
        if sentiment == "positive":
            return self._positive_insight(keyword_text, domain, category, product)

        # -------- NEGATIVE --------
        elif sentiment == "negative":
            return self._negative_insight(keyword_text, domain, category, product)

        # -------- NEUTRAL --------
        elif sentiment == "neutral":
            return self._neutral_insight(keyword_text, domain, category, product)

        return "Unable to generate insight."

    # -----------------------------
    # Positive Insight
    # -----------------------------
    def _positive_insight(self, keywords, domain, category, product):
        if product:
            return f"Customers are satisfied with {product}, highlighting strengths such as {keywords}."

        if category:
            return f"Positive feedback indicates strong performance in {category}, especially in {keywords}."

        return f"Users are generally satisfied, particularly appreciating {keywords}."

    # -----------------------------
    # Negative Insight
    # -----------------------------
    def _negative_insight(self, keywords, domain, category, product):
        if product:
            return f"Users are facing issues with {product}, mainly related to {keywords}."

        if category:
            return f"Negative feedback suggests problems in {category}, especially concerning {keywords}."

        return f"Customers are experiencing issues, mainly related to {keywords}."

    # -----------------------------
    # Neutral Insight
    # -----------------------------
    def _neutral_insight(self, keywords, domain, category, product):
        if product:
            return f"Feedback for {product} is mixed, mentioning aspects like {keywords}."

        if category:
            return f"Mixed responses observed in {category}, with mentions of {keywords}."

        return f"Feedback is neutral with no strong positive or negative signals, mentioning {keywords}."