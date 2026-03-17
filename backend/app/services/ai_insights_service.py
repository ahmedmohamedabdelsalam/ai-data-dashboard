import json
from typing import Dict, Any, Optional
from openai import OpenAI
from app.core.logging import logger
from app.models.schemas import AIInsightsResponse
from app.config.settings import settings

def generate_ai_insights(
    summary: Dict[str, Any], correlation: Optional[Dict], anomalies: Optional[Dict]
) -> AIInsightsResponse:
    """Generate LLM insights safely via OpenRouter API using OpenAI SDK."""
    logger.info("Starting AI insights generation via OpenRouter (OpenAI SDK).")

    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        logger.warning("AI insights disabled: missing OPENROUTER_API_KEY")
        return AIInsightsResponse(
            status="disabled",
            reason="missing_api_key",
            message="AI insights are disabled because OPENROUTER_API_KEY is not configured.",
            summary="AI generation disabled.",
            report="Please configure your OpenRouter API Key to enable this feature."
        )

    prompt = f"""You are a senior data analyst.
Analyze the dataset summary, correlations, and anomalies.
Return insights including:
- Key patterns
- Important correlations
- Possible causes of anomalies
- Business recommendations.

DATASET SUMMARY:
{json.dumps(summary, default=str)}

CORRELATIONS:
{json.dumps(correlation, default=str) if correlation else "None"}

ANOMALIES:
{json.dumps(anomalies, default=str) if anomalies else "None"}

IMPORTANT: Return ONLY a valid JSON object matching exactly this structure, with no markdown formatting or extra text:
{{
 "summary": "...",
 "key_patterns": "...",
 "correlation_insights": "...",
 "anomaly_explanations": "...",
 "recommendations": "..."
}}
"""

    try:
        # Initialize client pointed at OpenRouter
        logger.info(f"Using model: {settings.LLM_MODEL}")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:3000", # Optional, for OpenRouter rankings
                "X-Title": "AI Data Analysis Dashboard", # Optional
            }
        )

        logger.info("Sending request to OpenRouter...")
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} if "mistral" not in settings.LLM_MODEL.lower() else None # Mistral-tiny/small sometimes fail with json_object
        )

        content = response.choices[0].message.content.strip()
        
        # Remove possible markdown code block wraps
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        parsed_json = json.loads(content.strip())
        
        summary_text = parsed_json.get("summary", "Analysis complete.")
        key_patterns = parsed_json.get("key_patterns", "")
        correlation_insights = parsed_json.get("correlation_insights", "")
        anomaly_explanations = parsed_json.get("anomaly_explanations", "")
        recommendations = parsed_json.get("recommendations", "")
        
        # Build unified report string for frontend compatibility
        report_parts = []
        if key_patterns: report_parts.append(f"### Key Patterns\n{key_patterns}")
        if correlation_insights: report_parts.append(f"### Correlations\n{correlation_insights}")
        if anomaly_explanations: report_parts.append(f"### Anomalies\n{anomaly_explanations}")
        if recommendations: report_parts.append(f"### Recommendations\n{recommendations}")
        
        report_str = "\n\n".join(report_parts)
        
        logger.info("Successfully gathered AI insights from OpenRouter via SDK.")
        return AIInsightsResponse(
            summary=summary_text,
            report=report_str,
            key_patterns=key_patterns,
            correlation_insights=correlation_insights,
            anomaly_explanations=anomaly_explanations,
            recommendations=recommendations
        )

    except Exception as e:
        import traceback
        error_msg = f"Error generating AI insights through OpenRouter SDK: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return AIInsightsResponse(
            status="error",
            reason="insights_failed",
            message=str(e),
            summary="Error analyzing dataset.",
            report=f"An error occurred while communicating with the AI model: {str(e)}"
        )
