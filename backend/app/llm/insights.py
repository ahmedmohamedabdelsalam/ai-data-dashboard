"""
LLM integration for generating natural language insights (OpenAI or Gemini).
"""
from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd

from app.config.settings import settings
from app.models.schemas import AIInsightsResponse


def _build_context(df: pd.DataFrame, summary: Optional[Dict] = None, correlation: Optional[Dict] = None) -> str:
    """Build text context for LLM from dataset and optional analysis."""
    lines = [
        "## Dataset shape",
        f"- Rows: {len(df)}, Columns: {len(df.columns)}",
        "",
        "## Column dtypes",
        df.dtypes.astype(str).to_string(),
        "",
        "## Sample (first 5 rows)",
        df.head().to_string(),
        "",
        "## Numeric summary (describe)",
        df.select_dtypes(include=["number"]).describe().to_string() if df.select_dtypes(include=["number"]).shape[1] else "No numeric columns.",
    ]
    if summary:
        lines.extend(["", "## Summary stats", str(summary)])
    if correlation:
        lines.extend(["", "## Correlation (sample)", str(list(correlation.keys())[:5])])
    return "\n".join(lines)


def _call_openai(context: str) -> str:
    """Call OpenAI API for insights. Requires OPENAI_API_KEY."""
    try:
        from openai import OpenAI
    except ImportError:
        return "OpenAI package not installed. pip install openai"

    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return "OPENAI_API_KEY not set. Set it in environment to enable AI insights."

    try:
        client = OpenAI(api_key=api_key)
        prompt = f"""You are a data analyst. Based on the following dataset information, provide a concise, human-readable report.

Include:
1. A short summary of what the dataset appears to represent (2-3 sentences).
2. Notable correlations or patterns if numeric columns are present.
3. Data quality notes (missing values, types).
4. Two or three practical insights or recommendations.

Keep the report under 400 words. Be specific and reference column names where relevant.

Dataset information:
{context}
"""

        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
        )
        return response.choices[0].message.content or "No response from model."
    except Exception as e:
        return f"OpenAI API Request Failed: {str(e)}"


def _call_gemini(context: str) -> str:
    """Call Gemini API for insights. Requires GEMINI_API_KEY."""
    try:
        import google.generativeai as genai
    except ImportError:
        return "Google Generative AI package not installed. pip install google-generativeai"

    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return "GEMINI_API_KEY not set. Set it in environment to enable AI insights."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(settings.LLM_MODEL)
    prompt = f"""You are a data analyst. Based on the following dataset information, provide a concise, human-readable report.

Include:
1. A short summary of what the dataset appears to represent (2-3 sentences).
2. Notable correlations or patterns if numeric columns are present.
3. Data quality notes (missing values, types).
4. Two or three practical insights or recommendations.

Keep the report under 400 words. Be specific and reference column names where relevant.

Dataset information:
{context}
"""
    response = model.generate_content(prompt)
    if response and response.text:
        return response.text
    return "No response from model."


def generate_ai_insights(
    df: pd.DataFrame,
    summary: Optional[Dict[str, Any]] = None,
    correlation: Optional[Dict] = None,
) -> AIInsightsResponse:
    """
    Generate natural language insights using configured LLM (OpenAI or Gemini).
    """
    context = _build_context(df, summary=summary, correlation=correlation)
    provider = (settings.LLM_PROVIDER or "openai").lower()

    if provider == "gemini":
        report = _call_gemini(context)
    else:
        report = _call_openai(context)

    # First paragraph as summary
    summary_text = report.split("\n\n")[0] if report else "No insights generated."
    return AIInsightsResponse(
        summary=summary_text,
        correlations_explained=None,
        report=report,
        generated_at=datetime.utcnow().isoformat() + "Z",
    )
