from pathlib import Path
from datetime import datetime
import pandas as pd


def write_log(
    log_file,
    file_name,
    stage,
    status,
    row_count=None,
    message=""
):
    """
    Writes one record into an audit log CSV file.
    """

    # Convert the log file path into a Path object
    log_path = Path(log_file)

    # Make sure the logs folder exists
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create one log record
    log_record = pd.DataFrame([{
        "timestamp": datetime.now(),
        "file_name": file_name,
        "stage": stage,
        "status": status,
        "row_count": row_count,
        "message": message
    }])

    # If the log file already exists,
    # append the new record
    if log_path.exists():

        log_record.to_csv(
            log_path,
            mode="a",
            header=False,
            index=False
        )

    # Otherwise create a new file
    else:

        log_record.to_csv(
            log_path,
            mode="w",
            header=True,
            index=False
        )


def log_ingestion(
    file_name,
    status,
    row_count=None,
    message=""
):
    """
    Creates an ingestion log.
    """

    write_log(
        "logs/ingestion_log.csv",
        file_name,
        "INGESTION",
        status,
        row_count,
        message
    )


def log_preprocess(
    file_name,
    status,
    row_count=None,
    message=""
):
    """
    Creates a preprocessing log.
    """

    write_log(
        "logs/preprocess_log.csv",
        file_name,
        "PREPROCESSING",
        status,
        row_count,
        message
    )


def log_retention(
    file_name,
    status,
    row_count=None,
    message=""
):
    """
    Creates a retention log.
    """

    write_log(
        "logs/retention_log.csv",
        file_name,
        "RETENTION",
        status,
        row_count,
        message
    )

    