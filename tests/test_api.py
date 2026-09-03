import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Mock history service while importing app.main
mock_history_service = MagicMock()

mock_history_service.initialize_database = MagicMock()

TEST_HISTORY = [
    100, 110, 98, 95, 102,
    105, 108, 97, 99, 101
]

mock_history_service.get_history.return_value = TEST_HISTORY

# Save the real module if it has already been imported
real_history_service = sys.modules.get(
    "app.services.history_service"
)

sys.modules["app.services.history_service"] = (
    mock_history_service
)


from fastapi.testclient import TestClient
from app.main import app


# Restore the real history service immediately
if real_history_service is not None:
    sys.modules["app.services.history_service"] = (
        real_history_service
)
else:
    del sys.modules["app.services.history_service"]


client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_history():
    mock_history_service.get_history.return_value = TEST_HISTORY


def test_health_endpoint():
    response = client.get("/health/")

    assert response.status_code == 200


def test_analyze_endpoint():
    response = client.post(
        "/analyze/",
        json={"current_value": 105}
    )

    assert response.status_code == 200

    data = response.json()

    assert "baseline" in data
    assert "anomaly" in data
    assert "risk" in data
    assert "validation" in data

    assert data["validation"]["validation_status"] == "Pass"


def test_analyze_endpoint_detects_anomaly():
    response = client.post(
        "/analyze/",
        json={"current_value": 150}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["anomaly"]["status"] == "Anomaly"
    assert data["validation"]["validation_status"] == "Fail"