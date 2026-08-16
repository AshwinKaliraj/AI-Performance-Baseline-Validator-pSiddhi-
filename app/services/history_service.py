import sqlite3
from datetime import datetime


DB_PATH = "/data/performance_history.db"


performance_history = [
    100,
    110,
    98,
    95,
    102,
    105,
    108,
    97,
    99,
    101
]


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            response_time REAL NOT NULL,

            moving_average REAL NOT NULL,

            standard_deviation REAL NOT NULL,

            z_score REAL NOT NULL,

            risk_score REAL NOT NULL,

            risk_level TEXT NOT NULL,

            validation_status TEXT NOT NULL

        )
        """
    )

    connection.commit()

    connection.close()


def add_history(response_time):

    performance_history.append(response_time)

    return {
        "message": "Performance sample stored successfully.",
        "response_time": response_time
    }


def add_analysis_record(
    response_time,
    moving_average,
    standard_deviation,
    z_score,
    risk_score,
    risk_level,
    validation_status
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history (
            timestamp,
            response_time,
            moving_average,
            standard_deviation,
            z_score,
            risk_score,
            risk_level,
            validation_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            response_time,
            moving_average,
            standard_deviation,
            z_score,
            risk_score,
            risk_level,
            validation_status
        )
    )

    connection.commit()

    connection.close()


def get_history():

    return performance_history


def get_analysis_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            timestamp,
            response_time,
            moving_average,
            standard_deviation,
            z_score,
            risk_score,
            risk_level,
            validation_status
        FROM analysis_history
        ORDER BY id ASC
        """
    )

    records = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return records


def get_deviation_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            timestamp,
            response_time,
            moving_average,
            standard_deviation,
            z_score,
            risk_score,
            risk_level,
            validation_status
        FROM analysis_history
        WHERE ABS(z_score) >= 2
        ORDER BY id ASC
        """
    )

    records = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return records


def get_trend_analysis():

    records = get_analysis_history()

    if not records:

        return {
            "total_samples": 0,
            "average_response_time": 0,
            "maximum_response_time": 0,
            "average_risk_score": 0,
            "anomaly_count": 0,
            "warning_count": 0,
            "critical_count": 0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
            "pass_count": 0,
            "fail_count": 0,
            "anomaly_rate": 0,
            "latest": None
        }

    total_samples = len(records)

    response_times = [
        record["response_time"]
        for record in records
    ]

    risk_scores = [
        record["risk_score"]
        for record in records
    ]

    anomaly_count = sum(
        1
        for record in records
        if abs(record["z_score"]) >= 3
    )

    warning_count = sum(
        1
        for record in records
        if 2 <= abs(record["z_score"]) < 3
    )

    critical_count = sum(
        1
        for record in records
        if record["risk_level"] == "Critical"
    )

    high_risk_count = sum(
        1
        for record in records
        if record["risk_level"] == "High"
    )

    medium_risk_count = sum(
        1
        for record in records
        if record["risk_level"] == "Medium"
    )

    low_risk_count = sum(
        1
        for record in records
        if record["risk_level"] == "Low"
    )

    pass_count = sum(
        1
        for record in records
        if record["validation_status"] == "Pass"
    )

    fail_count = sum(
        1
        for record in records
        if record["validation_status"] == "Fail"
    )

    anomaly_rate = round(
        (anomaly_count / total_samples) * 100,
        2
    )

    latest = records[-1]

    return {
        "total_samples": total_samples,

        "average_response_time": round(
            sum(response_times) / total_samples,
            2
        ),

        "maximum_response_time": max(
            response_times
        ),

        "average_risk_score": round(
            sum(risk_scores) / total_samples,
            2
        ),

        "anomaly_count": anomaly_count,

        "warning_count": warning_count,

        "critical_count": critical_count,

        "high_risk_count": high_risk_count,

        "medium_risk_count": medium_risk_count,

        "low_risk_count": low_risk_count,

        "pass_count": pass_count,

        "fail_count": fail_count,

        "anomaly_rate": anomaly_rate,

        "latest": latest
    }