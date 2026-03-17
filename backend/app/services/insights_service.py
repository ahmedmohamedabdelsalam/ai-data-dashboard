import pandas as pd
from typing import Dict, Any, Optional
from app.core.logging import logger
from app.models.schemas import AIInsightsResponse
from app.llm.insights import generate_ai_insights
from app.config.settings import settings

def generate_insights(
    df: pd.DataFrame, summary: Dict[str, Any], correlation: Optional[Dict]
) -> AIInsightsResponse:
    """Generate LLM insights safely, checking environment handles."""
    try:
        logger.info("Generating AI insights.")
        if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
            logger.warning("AI insights disabled: missing OPENAI_API_KEY")
            return AIInsightsResponse(
                status="disabled",
                reason="missing_api_key",
                message="AI insights are disabled because OPENAI_API_KEY is not configured.",
                summary="AI generation disabled.",
                report="Please configure your OpenAI API Key to enable this feature."
            )
            
        if settings.LLM_PROVIDER == "gemini" and not settings.GEMINI_API_KEY:
            logger.warning("AI insights disabled: missing GEMINI_API_KEY")
            return AIInsightsResponse(
                status="disabled",
                reason="missing_api_key",
                message="AI insights are disabled because GEMINI_API_KEY is not configured.",
                summary="AI generation disabled.",
                report="Please configure your Gemini API Key to enable this feature."
            )

        return generate_ai_insights(df, summary=summary, correlation=correlation)
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        return AIInsightsResponse(
            status="error",
            reason="insights_failed",
            message=str(e),
            summary="Error analyzing dataset.",
            report="An error occurred while communicating with the AI model."
        )
