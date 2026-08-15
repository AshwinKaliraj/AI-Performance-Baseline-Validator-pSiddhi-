import numpy as np

from sklearn.preprocessing import StandardScaler

from app.services import history_service

from app.utils.prometheus_metrics import (
    BASELINE_MOVING_AVERAGE,
    BASELINE_STANDARD_DEVIATION
)


def calculate_baseline():

    historical_response_times = history_service.get_history()

    if not historical_response_times:
        return {
            "moving_average": 0,
            "standard_deviation": 0,
            "current_value": 0,
            "z_score": 0,
            "status": "Normal"
        }

    current_value = historical_response_times[-1]

    # Convert historical response times into a NumPy array
    response_times = np.array(
        historical_response_times,
        dtype=float
    ).reshape(-1, 1)

    # -----------------------------
    # Moving Average
    # -----------------------------

    moving_average = round(
        float(np.mean(response_times)),
        2
    )

    # -----------------------------
    # Standard Deviation
    # -----------------------------

    standard_deviation = round(
        float(np.std(response_times, ddof=1)),
        2
    )

    # -----------------------------
    # Z-Score using scikit-learn
    # -----------------------------

    if standard_deviation == 0:

        z_score = 0

    else:

        scaler = StandardScaler()

        scaler.fit(response_times)

        transformed_value = scaler.transform(
            np.array([[current_value]], dtype=float)
        )

        z_score = round(
            float(transformed_value[0][0]),
            2
        )

    # -----------------------------
    # Determine Status
    # -----------------------------

    if abs(z_score) < 2:

        status = "Normal"

    elif abs(z_score) < 3:

        status = "Warning"

    else:

        status = "Anomaly"

    # -----------------------------
    # Debug
    # -----------------------------

    print("========== BASELINE ==========")
    print("Moving Average      :", moving_average)
    print("Standard Deviation  :", standard_deviation)
    print("Current Value       :", current_value)
    print("Z Score             :", z_score)
    print("================================")

    # -----------------------------
    # Update Prometheus Metrics
    # -----------------------------

    BASELINE_MOVING_AVERAGE.set(
        moving_average
    )

    BASELINE_STANDARD_DEVIATION.set(
        standard_deviation
    )

    print("Baseline Prometheus Gauges Updated")
    print("===============================")

    return {

        "moving_average": moving_average,

        "standard_deviation": standard_deviation,

        "current_value": current_value,

        "z_score": z_score,

        "status": status

    }