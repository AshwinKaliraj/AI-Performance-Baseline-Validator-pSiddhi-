import sqlite3
from app.services import history_service


def setup_test_database(monkeypatch, tmp_path):
    db_path = tmp_path / "test_history.db"
    monkeypatch.setattr(
        history_service,
        "DB_PATH",
        str(db_path)
    )
    return db_path


def test_initialize_database(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    connection = sqlite3.connect(history_service.DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM performance_history"
    )
    count = cursor.fetchone()[0]

    assert count == len(
        history_service.INITIAL_PERFORMANCE_HISTORY
    )

    connection.close()


def test_initialize_database_does_not_duplicate_data(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()
    history_service.initialize_database()

    connection = sqlite3.connect(history_service.DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM performance_history"
    )
    count = cursor.fetchone()[0]

    assert count == len(
        history_service.INITIAL_PERFORMANCE_HISTORY
    )

    connection.close()


def test_get_connection(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    connection = history_service.get_connection()

    assert isinstance(connection, sqlite3.Connection)

    connection.close()


def test_add_history(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    result = history_service.add_history(125)

    assert result["message"] == (
        "Performance sample stored successfully."
    )
    assert result["response_time"] == 125

    history = history_service.get_history()

    assert history[-1] == 125


def test_get_history(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    history = history_service.get_history()

    assert len(history) == 10
    assert history == [
        float(value)
        for value in history_service.INITIAL_PERFORMANCE_HISTORY
    ]


def test_add_analysis_record(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    history_service.add_analysis_record(
        response_time=120,
        moving_average=105,
        standard_deviation=5,
        z_score=3,
        risk_score=80,
        risk_level="High",
        validation_status="Fail"
    )

    records = history_service.get_analysis_history()

    assert len(records) == 1
    assert records[0]["response_time"] == 120
    assert records[0]["moving_average"] == 105
    assert records[0]["standard_deviation"] == 5
    assert records[0]["z_score"] == 3
    assert records[0]["risk_score"] == 80
    assert records[0]["risk_level"] == "High"
    assert records[0]["validation_status"] == "Fail"


def test_get_analysis_history_empty(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    records = history_service.get_analysis_history()

    assert records == []


def test_get_deviation_history(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    history_service.add_analysis_record(
        100, 100, 5, 1, 20, "Low", "Pass"
    )

    history_service.add_analysis_record(
        120, 100, 5, 2.5, 50, "Medium", "Warning"
    )

    history_service.add_analysis_record(
        140, 100, 5, 4, 90, "Critical", "Fail"
    )

    records = history_service.get_deviation_history()

    assert len(records) == 2
    assert records[0]["z_score"] == 2.5
    assert records[1]["z_score"] == 4


def test_get_trend_analysis_no_data(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    result = history_service.get_trend_analysis()

    assert result["total_samples"] == 0
    assert result["anomaly_count"] == 0
    assert result["response_time_trend"] == "No Data"
    assert result["risk_trend"] == "No Data"
    assert result["anomaly_trend"] == "No Data"
    assert result["latest"] is None


def test_get_trend_analysis_with_data(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    history_service.add_analysis_record(
        100, 100, 5, 0, 10, "Low", "Pass"
    )
    history_service.add_analysis_record(
        110, 100, 5, 2.5, 40, "Medium", "Warning"
    )
    history_service.add_analysis_record(
        130, 100, 5, 3.5, 70, "High", "Fail"
    )
    history_service.add_analysis_record(
        150, 100, 5, 4.5, 90, "Critical", "Fail"
    )

    result = history_service.get_trend_analysis()

    assert result["total_samples"] == 4
    assert result["maximum_response_time"] == 150
    assert result["anomaly_count"] == 2
    assert result["warning_count"] == 1
    assert result["critical_count"] == 1
    assert result["high_risk_count"] == 1
    assert result["medium_risk_count"] == 1
    assert result["low_risk_count"] == 1
    assert result["pass_count"] == 1
    assert result["fail_count"] == 2
    assert result["anomaly_rate"] == 50
    assert result["latest"]["response_time"] == 150


def test_get_trend_analysis_single_record(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    history_service.add_analysis_record(
        100, 100, 5, 0, 20, "Low", "Pass"
    )

    result = history_service.get_trend_analysis()

    assert result["total_samples"] == 1
    assert result["recent_average_response_time"] == 100
    assert result["previous_average_response_time"] == 100
    assert result["recent_average_risk_score"] == 20
    assert result["previous_average_risk_score"] == 20
    assert result["response_time_change_percent"] == 0
    assert result["risk_score_change_percent"] == 0
    assert result["response_time_trend"] == "Stable"
    assert result["risk_trend"] == "Stable"
    assert result["anomaly_trend"] == "Stable"
    assert result["consecutive_anomalies"] == 0


def test_get_trend_analysis_consecutive_anomalies(
    monkeypatch,
    tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    history_service.initialize_database()

    history_service.add_analysis_record(
        100, 100, 5, 0, 10, "Low", "Pass"
    )
    history_service.add_analysis_record(
        130, 100, 5, 3.5, 70, "High", "Fail"
    )
    history_service.add_analysis_record(
        140, 100, 5, 4, 80, "Critical", "Fail"
    )
    history_service.add_analysis_record(
        150, 100, 5, 5, 90, "Critical", "Fail"
    )

    result = history_service.get_trend_analysis()

    assert result["consecutive_anomalies"] == 3