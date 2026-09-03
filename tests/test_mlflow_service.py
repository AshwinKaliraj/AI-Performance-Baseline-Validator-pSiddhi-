import hashlib
from types import SimpleNamespace

from app.services import mlflow_service


def test_initialize(monkeypatch, tmp_path):
    tracking_uri = f"sqlite:///{tmp_path / 'mlflow.db'}"

    monkeypatch.setattr(
        mlflow_service,
        "DATA_DIR",
        str(tmp_path)
    )
    monkeypatch.setattr(
        mlflow_service,
        "TRACKING_URI",
        tracking_uri
    )

    calls = []

    monkeypatch.setattr(
        mlflow_service.mlflow,
        "set_tracking_uri",
        lambda uri: calls.append(("tracking_uri", uri))
    )

    monkeypatch.setattr(
        mlflow_service.mlflow,
        "set_experiment",
        lambda name: calls.append(("experiment", name))
    )

    mlflow_service.initialize()

    assert ("tracking_uri", tracking_uri) in calls
    assert (
        "experiment",
        mlflow_service.EXPERIMENT_NAME
    ) in calls


def test_generate_baseline_signature():
    result = mlflow_service._generate_baseline_signature(
        103.18,
        7.22
    )

    expected = hashlib.sha256(
        "103.18|7.22".encode("utf-8")
    ).hexdigest()[:12]

    assert result == expected
    assert len(result) == 12


def test_get_baseline_version_experiment_not_initialized(
    monkeypatch
):
    monkeypatch.setattr(
        mlflow_service,
        "_get_experiment",
        lambda: None
    )

    try:
        mlflow_service._get_baseline_version(
            100,
            5
        )
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert str(exc) == (
            "MLflow experiment is not initialized."
        )


def test_get_baseline_version_existing(
    monkeypatch
):
    experiment = SimpleNamespace(
        experiment_id="1"
    )

    existing_run = SimpleNamespace(
        data=SimpleNamespace(
            tags={
                "baseline_version": "v2"
            }
        )
    )

    class FakeClient:
        def search_runs(
            self,
            experiment_ids,
            filter_string=None,
            order_by=None,
            max_results=None
        ):
            return [existing_run]

    monkeypatch.setattr(
        mlflow_service,
        "_get_experiment",
        lambda: experiment
    )

    monkeypatch.setattr(
        mlflow_service,
        "MlflowClient",
        FakeClient
    )

    version, signature = (
        mlflow_service._get_baseline_version(
            103.18,
            7.22
        )
    )

    assert version == "v2"
    assert signature == (
        mlflow_service._generate_baseline_signature(
            103.18,
            7.22
        )
    )


def test_get_baseline_version_new(
    monkeypatch
):
    experiment = SimpleNamespace(
        experiment_id="1"
    )

    run1 = SimpleNamespace(
        data=SimpleNamespace(
            tags={
                "baseline_version": "v2"
            }
        )
    )

    run2 = SimpleNamespace(
        data=SimpleNamespace(
            tags={
                "baseline_version": "v1"
            }
        )
    )

    class FakeClient:
        def search_runs(
            self,
            experiment_ids,
            filter_string=None,
            order_by=None,
            max_results=None
        ):
            if filter_string:
                return []

            return [run1, run2]

    monkeypatch.setattr(
        mlflow_service,
        "_get_experiment",
        lambda: experiment
    )

    monkeypatch.setattr(
        mlflow_service,
        "MlflowClient",
        FakeClient
    )

    version, signature = (
        mlflow_service._get_baseline_version(
            110,
            8
        )
    )

    assert version == "v3"
    assert signature == (
        mlflow_service._generate_baseline_signature(
            110,
            8
        )
    )


def test_get_baseline_version_new_without_versions(
    monkeypatch
):
    experiment = SimpleNamespace(
        experiment_id="1"
    )

    class FakeClient:
        def search_runs(
            self,
            experiment_ids,
            filter_string=None,
            order_by=None,
            max_results=None
        ):
            return []

    monkeypatch.setattr(
        mlflow_service,
        "_get_experiment",
        lambda: experiment
    )

    monkeypatch.setattr(
        mlflow_service,
        "MlflowClient",
        FakeClient
    )

    version, signature = (
        mlflow_service._get_baseline_version(
            100,
            5
        )
    )

    assert version == "v1"
    assert len(signature) == 12


def test_log_analysis(monkeypatch):
    calls = []

    monkeypatch.setattr(
        mlflow_service,
        "_get_baseline_version",
        lambda ma, sd: ("v2", "abc123")
    )

    class FakeRun:
        info = SimpleNamespace(
            run_id="test-run-123"
        )

        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc_value,
            traceback
        ):
            return False

    fake_run = FakeRun()

    monkeypatch.setattr(
        mlflow_service.mlflow,
        "start_run",
        lambda: fake_run
    )

    monkeypatch.setattr(
        mlflow_service.mlflow,
        "log_metric",
        lambda name, value: calls.append(
            ("metric", name, value)
        )
    )

    monkeypatch.setattr(
        mlflow_service.mlflow,
        "log_param",
        lambda name, value: calls.append(
            ("param", name, value)
        )
    )

    monkeypatch.setattr(
        mlflow_service.mlflow,
        "set_tag",
        lambda name, value: calls.append(
            ("tag", name, value)
        )
    )

    result = mlflow_service.log_analysis(
        response_time=120,
        moving_average=105,
        standard_deviation=5,
        z_score=3,
        risk_score=80,
        risk_level="High",
        validation_status="Fail"
    )

    assert result["run_id"] == "test-run-123"
    assert result["baseline_version"] == "v2"
    assert result["moving_average"] == 105
    assert result["standard_deviation"] == 5

    assert (
        "metric",
        "response_time",
        120
    ) in calls

    assert (
        "metric",
        "moving_average",
        105
    ) in calls

    assert (
        "metric",
        "standard_deviation",
        5
    ) in calls

    assert (
        "metric",
        "z_score",
        3
    ) in calls

    assert (
        "metric",
        "risk_score",
        80
    ) in calls

    assert (
        "param",
        "risk_level",
        "High"
    ) in calls

    assert (
        "param",
        "validation_status",
        "Fail"
    ) in calls

    assert (
        "tag",
        "baseline_version",
        "v2"
    ) in calls

    assert (
        "tag",
        "baseline_signature",
        "abc123"
    ) in calls


def test_get_baseline_versions_no_experiment(
    monkeypatch
):
    monkeypatch.setattr(
        mlflow_service,
        "_get_experiment",
        lambda: None
    )

    assert mlflow_service.get_baseline_versions() == []


def test_get_baseline_versions(
    monkeypatch
):
    experiment = SimpleNamespace(
        experiment_id="1"
    )

    run1 = SimpleNamespace(
        data=SimpleNamespace(
            tags={"baseline_version": "v1"},
            metrics={
                "moving_average": 101.5,
                "standard_deviation": 4.84
            }
        ),
        info=SimpleNamespace(
            run_id="run-1",
            start_time=1000
        )
    )

    run1_duplicate = SimpleNamespace(
        data=SimpleNamespace(
            tags={"baseline_version": "v1"},
            metrics={
                "moving_average": 999,
                "standard_deviation": 999
            }
        ),
        info=SimpleNamespace(
            run_id="run-duplicate",
            start_time=2000
        )
    )

    run2 = SimpleNamespace(
        data=SimpleNamespace(
            tags={"baseline_version": "v2"},
            metrics={
                "moving_average": 103.18,
                "standard_deviation": 7.22
            }
        ),
        info=SimpleNamespace(
            run_id="run-2",
            start_time=3000
        )
    )

    run_without_version = SimpleNamespace(
        data=SimpleNamespace(
            tags={},
            metrics={}
        ),
        info=SimpleNamespace(
            run_id="run-3",
            start_time=4000
        )
    )

    class FakeClient:
        def search_runs(
            self,
            experiment_ids,
            order_by=None
        ):
            return [
                run1,
                run1_duplicate,
                run2,
                run_without_version
            ]

    monkeypatch.setattr(
        mlflow_service,
        "_get_experiment",
        lambda: experiment
    )

    monkeypatch.setattr(
        mlflow_service,
        "MlflowClient",
        FakeClient
    )

    result = mlflow_service.get_baseline_versions()

    assert len(result) == 2

    assert result[0]["baseline_version"] == "v1"
    assert result[0]["run_id"] == "run-1"
    assert result[0]["moving_average"] == 101.5

    assert result[1]["baseline_version"] == "v2"
    assert result[1]["run_id"] == "run-2"
    assert result[1]["moving_average"] == 103.18


def test_compare_baseline_versions_not_available(
    monkeypatch
):
    monkeypatch.setattr(
        mlflow_service,
        "get_baseline_versions",
        lambda: [
            {
                "baseline_version": "v1",
                "moving_average": 100,
                "standard_deviation": 5
            }
        ]
    )

    result = (
        mlflow_service.compare_baseline_versions()
    )

    assert result["comparison_available"] is False
    assert "At least two baseline versions" in (
        result["message"]
    )


def test_compare_baseline_versions(
    monkeypatch
):
    monkeypatch.setattr(
        mlflow_service,
        "get_baseline_versions",
        lambda: [
            {
                "baseline_version": "v1",
                "moving_average": 100,
                "standard_deviation": 5
            },
            {
                "baseline_version": "v2",
                "moving_average": 103.18,
                "standard_deviation": 7.22
            }
        ]
    )

    result = (
        mlflow_service.compare_baseline_versions()
    )

    assert result["comparison_available"] is True
    assert (
        result["previous_version"]["baseline_version"]
        == "v1"
    )
    assert (
        result["latest_version"]["baseline_version"]
        == "v2"
    )
    assert (
        result["difference"]["moving_average"]
        == 3.18
    )
    assert (
        result["difference"]["standard_deviation"]
        == 2.22
    )