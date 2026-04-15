from fastapi import FastAPI
from pydantic import BaseModel

# Import services
from app.services.prediction_service import PredictionService
from app.services.insight_service import InsightService
from app.services.chatbot_service import ChatbotService

# Initialize app
app = FastAPI(title="AI Feedback Intelligence API")

# Initialize services
prediction_service = PredictionService()
insight_service = InsightService()
chatbot_service = ChatbotService()


# -----------------------------
# Request Schema
# -----------------------------
class FeedbackRequest(BaseModel):
    text: str
    domain: str = None
    category: str = None
    product: str = None


# -----------------------------
# Root Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI Feedback Analyzer API is running 🚀"}


# -----------------------------
# Prediction Route
# -----------------------------
@app.post("/predict")
def predict_feedback(request: FeedbackRequest):

    # -------- Step 1: Prediction --------
    result = prediction_service.predict(request.text)

    if "error" in result:
        return result

    sentiment = result["sentiment"]
    confidence = result["confidence"]
    keywords = result["keywords"]

    # -------- Step 2: Insight --------
    insight = insight_service.generate_insight(
        sentiment=sentiment,
        keywords=keywords,
        domain=request.domain,
        category=request.category,
        product=request.product
    )

    # -------- Step 3: Chatbot Response --------
    response = chatbot_service.generate_response(
        sentiment=sentiment,
        keywords=keywords,
        product=request.product
    )

    # -------- Final Output --------
    return {
        "input_text": request.text,
        "sentiment": sentiment,
        "confidence": confidence,
        "keywords": keywords,
        "insight": insight,
        "response": response,
        "context": {
            "domain": request.domain,
            "category": request.category,
            "product": request.product
        }
    }