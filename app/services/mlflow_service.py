import hashlib
import os

import mlflow
from mlflow.tracking import MlflowClient


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


def _get_experiment():

    return mlflow.get_experiment_by_name(
        EXPERIMENT_NAME
    )


def _generate_baseline_signature(
    moving_average,
    standard_deviation
):

    signature = (
        f"{moving_average}|"
        f"{standard_deviation}"
    )

    return hashlib.sha256(
        signature.encode("utf-8")
    ).hexdigest()[:12]


def _get_baseline_version(
    moving_average,
    standard_deviation
):

    experiment = _get_experiment()

    if experiment is None:

        raise RuntimeError(
            "MLflow experiment is not initialized."
        )

    client = MlflowClient()

    baseline_signature = (
        _generate_baseline_signature(
            moving_average,
            standard_deviation
        )
    )

    runs = client.search_runs(
        experiment_ids=[
            experiment.experiment_id
        ],
        filter_string=(
            f"tags.baseline_signature = "
            f"'{baseline_signature}'"
        ),
        order_by=[
            "start_time DESC"
        ],
        max_results=1
    )

    # Existing baseline version
    if runs:

        existing_version = (
            runs[0].data.tags.get(
                "baseline_version"
            )
        )

        if existing_version:

            return (
                existing_version,
                baseline_signature
            )

    # New baseline version
    all_runs = client.search_runs(
        experiment_ids=[
            experiment.experiment_id
        ],
        order_by=[
            "start_time DESC"
        ]
    )

    versions = set()

    for run in all_runs:

        version = run.data.tags.get(
            "baseline_version"
        )

        if version:

            versions.add(version)

    version_number = len(versions) + 1

    baseline_version = (
        f"v{version_number}"
    )

    return (
        baseline_version,
        baseline_signature
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

    (
        baseline_version,
        baseline_signature
    ) = _get_baseline_version(
        moving_average,
        standard_deviation
    )

    with mlflow.start_run() as run:

        # -----------------------------
        # Metrics
        # -----------------------------

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

        # -----------------------------
        # Parameters
        # -----------------------------

        mlflow.log_param(
            "risk_level",
            risk_level
        )

        mlflow.log_param(
            "validation_status",
            validation_status
        )

        # -----------------------------
        # Baseline Version Tracking
        # -----------------------------

        mlflow.set_tag(
            "baseline_version",
            baseline_version
        )

        mlflow.set_tag(
            "baseline_signature",
            baseline_signature
        )

        mlflow.set_tag(
            "baseline_moving_average",
            str(moving_average)
        )

        mlflow.set_tag(
            "baseline_standard_deviation",
            str(standard_deviation)
        )

        print(
            "MLflow analysis logged successfully."
        )

        print(
            "Baseline Version:",
            baseline_version
        )

        print(
            "Run ID:",
            run.info.run_id
        )

    return {

        "run_id": run.info.run_id,

        "baseline_version": baseline_version,

        "moving_average": moving_average,

        "standard_deviation": standard_deviation

    }


def get_baseline_versions():

    experiment = _get_experiment()

    if experiment is None:

        return []

    client = MlflowClient()

    runs = client.search_runs(
        experiment_ids=[
            experiment.experiment_id
        ],
        order_by=[
            "start_time ASC"
        ]
    )

    versions = {}

    for run in runs:

        version = run.data.tags.get(
            "baseline_version"
        )

        if not version:
            continue

        if version not in versions:

            versions[version] = {
                "baseline_version": version,
                "run_id": run.info.run_id,
                "moving_average": run.data.metrics.get(
                    "moving_average"
                ),
                "standard_deviation": run.data.metrics.get(
                    "standard_deviation"
                ),
                "created_at": run.info.start_time
            }

    return list(
        versions.values()
    )


def compare_baseline_versions():

    versions = get_baseline_versions()

    if len(versions) < 2:

        return {
            "comparison_available": False,
            "message": (
                "At least two baseline "
                "versions are required "
                "for comparison."
            ),
            "versions": versions
        }

    previous_version = versions[-2]

    latest_version = versions[-1]

    moving_average_difference = round(
        latest_version["moving_average"]
        - previous_version["moving_average"],
        2
    )

    standard_deviation_difference = round(
        latest_version["standard_deviation"]
        - previous_version["standard_deviation"],
        2
    )

    return {

        "comparison_available": True,

        "previous_version": previous_version,

        "latest_version": latest_version,

        "difference": {

            "moving_average": (
                moving_average_difference
            ),

            "standard_deviation": (
                standard_deviation_difference
            )

        }

    }