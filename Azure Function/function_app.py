import azure.functions as func
import logging
import requests
import os
import json
from datetime import datetime
import sys

# Add FastAPI project path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(PROJECT_ROOT)

# Import history service only
from app.services import history_service

app = func.FunctionApp()


@app.timer_trigger(
    schedule="*/30 * * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def timer_trigger(myTimer: func.TimerRequest):

    if myTimer.past_due:
        logging.info("Timer is past due.")

    logging.info("Running scheduled baseline comparison...")

    try:

        # Get latest response time
        history = history_service.get_history()

        if not history:
            logging.warning("No performance history available.")
            return

        current_value = history[-1]

        logging.info(f"Latest Response Time: {current_value}")

        # ----------------------------------------
        # Call FastAPI Analyze API
        # ----------------------------------------

        response = requests.post(
            "http://localhost:8000/analyze/",
            json={
                "current_value": current_value
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        # ----------------------------------------
        # Save Report
        # ----------------------------------------

        reports_folder = os.path.join(PROJECT_ROOT, "reports")
        os.makedirs(reports_folder, exist_ok=True)

        filename = os.path.join(
            reports_folder,
            f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(filename, "w") as file:
            json.dump(result, file, indent=4)

        logging.info(f"Analysis report saved to {filename}")

        # Print AI explanations

        logging.info("========== GEMINI ==========")
        logging.info(result.get("gemini_explanation", "Not Found"))

        logging.info("========== GROQ ==========")
        logging.info(result.get("groq_explanation", "Not Found"))

        logging.info("Scheduled baseline comparison completed successfully.")

    except Exception as e:
        logging.exception(f"Timer Trigger Failed: {str(e)}")