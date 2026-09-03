from app.services import anomaly_service
from app.services import risk_service
from app.services import validation_service
from app.services import history_service


TEST_HISTORY = [
    100, 110, 98, 95, 102,
    105, 108, 97, 99, 101
]


def test_anomaly_normal_value(monkeypatch):
    monkeypatch.setattr(
        history_service,
        "get_history",
        lambda: TEST_HISTORY
    )

    result = anomaly_service.detect_anomaly(105)

    assert result["status"] == "Normal"
    assert result["z_score"] < 2


def test_risk_low_for_normal_value(monkeypatch):
    monkeypatch.setattr(
        history_service,
        "get_history",
        lambda: TEST_HISTORY
    )

    result = risk_service.calculate_risk(105)

    assert result["risk_level"] == "Low"
    assert result["risk_score"] == 20


def test_validation_pass_for_normal_value(monkeypatch):
    monkeypatch.setattr(
        history_service,
        "get_history",
        lambda: TEST_HISTORY
    )

    result = validation_service.validate_performance(105)

    assert result["validation_status"] == "Pass"
    assert result["risk_level"] == "Low"


def test_anomaly_critical_value(monkeypatch):
    monkeypatch.setattr(
        history_service,
        "get_history",
        lambda: TEST_HISTORY
    )

    result = anomaly_service.detect_anomaly(150)

    assert result["status"] == "Anomaly"
    assert result["z_score"] >= 2


def test_risk_critical_for_high_value(monkeypatch):
    monkeypatch.setattr(
        history_service,
        "get_history",
        lambda: TEST_HISTORY
    )

    result = risk_service.calculate_risk(150)

    assert result["risk_level"] in ["High", "Critical"]
    assert result["risk_score"] >= 60


def test_validation_fail_for_high_value(monkeypatch):
    monkeypatch.setattr(
        history_service,
        "get_history",
        lambda: TEST_HISTORY
    )

    result = validation_service.validate_performance(150)

    assert result["validation_status"] == "Fail"
    assert result["risk_level"] in ["High", "Critical"]