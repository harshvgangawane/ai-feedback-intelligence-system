# app/schemas/request_schema.py

from pydantic import BaseModel, Field
from typing import Optional


class FeedbackRequest(BaseModel):
    """
    Input schema for feedback prediction
    """

    text: str = Field(..., example="Battery drains fast but camera is good")

    domain: Optional[str] = Field(
        default=None,
        example="E-commerce",
        description="Domain of feedback (E-commerce, App, Service)"
    )

    category: Optional[str] = Field(
        default=None,
        example="Electronics",
        description="Category of product/service"
    )

    product: Optional[str] = Field(
        default=None,
        example="iPhone 13",
        description="Product or service name"
    )


class FeedbackResponse(BaseModel):
    """
    Output schema for prediction response
    """

    input_text: str
    sentiment: str
    confidence: Optional[float]
    keywords: list[str]
    insight: str
    response: str

    context: dict