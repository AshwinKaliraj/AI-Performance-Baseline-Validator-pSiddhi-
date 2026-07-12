import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_explanation(
    baseline,
    anomaly,
    risk,
    validation
):

    prompt = f"""
You are an AI Performance Monitoring Assistant.

Analyze the following performance metrics.

Current Response Time: {risk["current_value"]} ms
Moving Average: {baseline["moving_average"]} ms
Standard Deviation: {baseline["standard_deviation"]}
Z-Score: {risk["z_score"]}
Risk Score: {risk["risk_score"]}
Risk Level: {risk["risk_level"]}
Validation Status: {validation["validation_status"]}

Provide the response in plain text only.

Use exactly this format.

Summary:
<2 concise sentences>

Root Cause:
<Explain the likely cause>

Impact:
<Explain the business or technical impact>

Recommendation:
<Provide 2 or 3 actionable recommendations>

Rules:
- Do not use Markdown.
- Do not use ** or bullet points.
- Do not use numbered lists.
- Keep the response under 200 words.
- Make the explanation professional and concise.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text.strip()