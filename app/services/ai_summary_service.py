from datetime import datetime

latest_analysis = {

    "timestamp": "",

    "baseline": {},

    "anomaly": {},

    "risk": {},

    "validation": {},

    "recommendation": {},

    "gemini": "",

    "groq": ""

}


def update(
    baseline,
    anomaly,
    risk,
    validation,
    recommendation,
    gemini,
    groq
):

    latest_analysis["timestamp"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    latest_analysis["baseline"] = baseline

    latest_analysis["anomaly"] = anomaly

    latest_analysis["risk"] = risk

    latest_analysis["validation"] = validation

    latest_analysis["recommendation"] = recommendation

    latest_analysis["gemini"] = gemini

    latest_analysis["groq"] = groq


def get():

    return latest_analysis