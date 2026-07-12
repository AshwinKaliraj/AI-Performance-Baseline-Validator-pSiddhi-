import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
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

Provide the response in plain text.

Format:

Summary:
Root Cause:
Impact:
Recommendation:

Keep the explanation professional and under 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()