import sqlite3
from datetime import datetime


DB_PATH = "/data/performance_history.db"


INITIAL_PERFORMANCE_HISTORY = [
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
        CREATE TABLE IF NOT EXISTS performance_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            response_time REAL NOT NULL

        )
        """
    )

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

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM performance_history
        """
    )

    count = cursor.fetchone()["count"]

    if count == 0:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.executemany(
            """
            INSERT INTO performance_history (
                timestamp,
                response_time
            )
            VALUES (?, ?)
            """,
            [
                (
                    timestamp,
                    response_time
                )
                for response_time
                in INITIAL_PERFORMANCE_HISTORY
            ]
        )

    connection.commit()

    connection.close()


def add_history(response_time):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO performance_history (
            timestamp,
            response_time
        )
        VALUES (?, ?)
        """,
        (
            timestamp,
            response_time
        )
    )

    connection.commit()

    connection.close()

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

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT response_time
        FROM performance_history
        ORDER BY id ASC
        """
    )

    records = cursor.fetchall()

    connection.close()

    return [
        float(record["response_time"])
        for record in records
    ]


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
            "response_time_trend": "No Data",
            "risk_trend": "No Data",
            "anomaly_trend": "No Data",
            "recent_average_response_time": 0,
            "previous_average_response_time": 0,
            "response_time_change_percent": 0,
            "recent_average_risk_score": 0,
            "previous_average_risk_score": 0,
            "risk_score_change_percent": 0,
            "consecutive_anomalies": 0,
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

    # ---------------------------------
    # Recent vs Previous Trend
    # ---------------------------------

    comparison_window = min(
        5,
        total_samples // 2
    )

    if comparison_window > 0:

        previous_records = records[
            -comparison_window * 2:
            -comparison_window
        ]

        recent_records = records[
            -comparison_window:
        ]

        recent_response_average = round(
            sum(
                record["response_time"]
                for record in recent_records
            ) / len(recent_records),
            2
        )

        previous_response_average = round(
            sum(
                record["response_time"]
                for record in previous_records
            ) / len(previous_records),
            2
        )

        recent_risk_average = round(
            sum(
                record["risk_score"]
                for record in recent_records
            ) / len(recent_records),
            2
        )

        previous_risk_average = round(
            sum(
                record["risk_score"]
                for record in previous_records
            ) / len(previous_records),
            2
        )

    else:

        recent_response_average = round(
            response_times[-1],
            2
        )

        previous_response_average = round(
            response_times[-1],
            2
        )

        recent_risk_average = round(
            risk_scores[-1],
            2
        )

        previous_risk_average = round(
            risk_scores[-1],
            2
        )

    if previous_response_average != 0:

        response_time_change_percent = round(
            (
                (
                    recent_response_average
                    - previous_response_average
                )
                / previous_response_average
            ) * 100,
            2
        )

    else:

        response_time_change_percent = 0

    if previous_risk_average != 0:

        risk_score_change_percent = round(
            (
                (
                    recent_risk_average
                    - previous_risk_average
                )
                / previous_risk_average
            ) * 100,
            2
        )

    else:

        risk_score_change_percent = 0

    # ---------------------------------
    # Response Time Trend
    # ---------------------------------

    if response_time_change_percent > 5:

        response_time_trend = "Increasing"

    elif response_time_change_percent < -5:

        response_time_trend = "Decreasing"

    else:

        response_time_trend = "Stable"

    # ---------------------------------
    # Risk Trend
    # ---------------------------------

    if risk_score_change_percent > 5:

        risk_trend = "Increasing"

    elif risk_score_change_percent < -5:

        risk_trend = "Decreasing"

    else:

        risk_trend = "Stable"

    # ---------------------------------
    # Anomaly Trend
    # ---------------------------------

    recent_anomaly_count = sum(
        1
        for record in records[
            -comparison_window:
        ]
        if abs(record["z_score"]) >= 3
    ) if comparison_window > 0 else 0

    previous_anomaly_count = sum(
        1
        for record in records[
            -comparison_window * 2:
            -comparison_window
        ]
        if abs(record["z_score"]) >= 3
    ) if comparison_window > 0 else 0

    if recent_anomaly_count > previous_anomaly_count:

        anomaly_trend = "Increasing"

    elif recent_anomaly_count < previous_anomaly_count:

        anomaly_trend = "Decreasing"

    else:

        anomaly_trend = "Stable"

    # ---------------------------------
    # Consecutive Anomalies
    # ---------------------------------

    consecutive_anomalies = 0

    for record in reversed(records):

        if abs(record["z_score"]) >= 3:

            consecutive_anomalies += 1

        else:

            break

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

        "response_time_trend": response_time_trend,

        "risk_trend": risk_trend,

        "anomaly_trend": anomaly_trend,

        "recent_average_response_time":
            recent_response_average,

        "previous_average_response_time":
            previous_response_average,

        "response_time_change_percent":
            response_time_change_percent,

        "recent_average_risk_score":
            recent_risk_average,

        "previous_average_risk_score":
            previous_risk_average,

        "risk_score_change_percent":
            risk_score_change_percent,

        "consecutive_anomalies":
            consecutive_anomalies,

        "latest": latest
    }