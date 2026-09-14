from typing import Any

from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    symbol: str
    scoring_model_version: str
    overall_score: float
    recommendation: str
    overall_confidence: dict[str, Any]
    business_quality: dict[str, Any]
    valuation: dict[str, Any]
    strengths: list[str]
    weaknesses: list[str]
    warnings: list[str]
