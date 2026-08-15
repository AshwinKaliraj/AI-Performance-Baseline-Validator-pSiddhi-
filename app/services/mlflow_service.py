import os
import mlflow


EXPERIMENT_NAME = "AI Performance Baseline Validator"

DATA_DIR = "/data"

MLFLOW_DB = os.path.join(
    DATA_DIR,
    "mlflow.db"
)

TRACKING_URI = f"sqlite:///{MLFLOW_DB}"


def initialize():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    mlflow.set_tracking_uri(
        TRACKING_URI
    )

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    print(
        "MLflow initialized successfully."
    )

    print(
        f"MLflow Tracking URI: {TRACKING_URI}"
    )


def log_analysis(
    response_time,
    moving_average,
    standard_deviation,
    z_score,
    risk_score,
    risk_level,
    validation_status
):

    with mlflow.start_run():

        mlflow.log_metric(
            "response_time",
            response_time
        )

        mlflow.log_metric(
            "moving_average",
            moving_average
        )

        mlflow.log_metric(
            "standard_deviation",
            standard_deviation
        )

        mlflow.log_metric(
            "z_score",
            z_score
        )

        mlflow.log_metric(
            "risk_score",
            risk_score
        )

        mlflow.log_param(
            "risk_level",
            risk_level
        )

        mlflow.log_param(
            "validation_status",
            validation_status
        )

        print(
            "MLflow analysis logged successfully."
        )