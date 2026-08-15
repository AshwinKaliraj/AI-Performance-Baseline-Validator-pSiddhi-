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