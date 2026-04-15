# app/services/chatbot_service.py


class ChatbotService:
    def __init__(self):
        pass

    def generate_response(self, sentiment: str, keywords: list = None, domain=None, category=None, product=None):
        """
        Generate chatbot-style response based on sentiment + context
        """

        if not sentiment:
            return "I'm not sure how to respond to that."

        # Format keywords
        keyword_text = ", ".join(keywords) if keywords else "your feedback"

        # -------- POSITIVE --------
        if sentiment == "positive":
            return self._positive_response(keyword_text, product)

        # -------- NEGATIVE --------
        elif sentiment == "negative":
            return self._negative_response(keyword_text, product)

        # -------- NEUTRAL --------
        elif sentiment == "neutral":
            return self._neutral_response(keyword_text, product)

        return "Thanks for your input!"

    # -----------------------------
    # Positive Responses
    # -----------------------------
    def _positive_response(self, keywords, product):
        if product:
            return f"Glad you liked {product}! 😊 It's great to hear positive feedback about {keywords}."

        return f"Glad you had a good experience! 😊 Thanks for highlighting {keywords}."

    # -----------------------------
    # Negative Responses
    # -----------------------------
    def _negative_response(self, keywords, product):
        if product:
            return f"Sorry to hear about your experience with {product}. 😔 We'll look into issues related to {keywords}."

        return f"Sorry to hear that 😔 We'll try to improve issues related to {keywords}."

    # -----------------------------
    # Neutral Responses
    # -----------------------------
    def _neutral_response(self, keywords, product):
        if product:
            return f"Thanks for your feedback on {product}. 👍 We noted your comments about {keywords}."

        return f"Thanks for your feedback 👍 We'll consider your input regarding {keywords}."