from pathlib import Path
from datetime import datetime
import re


def get_project_root():
    """
    Returns the root folder of the project.
    """

    return Path(__file__).resolve().parent.parent


def get_current_timestamp():
    """
    Returns the current date and time.
    """

    return datetime.now()


def extract_file_date(file_name):
    """
    Extracts the date from a filename.

    Example:
    claims_20251017.csv

    Result:
    2025-10-17
    """

    match = re.search(
        r"_(\d{8})\.csv$",
        file_name
    )

    if not match:
        raise ValueError(
            f"Could not extract date from filename: {file_name}"
        )

    date_string = match.group(1)

    return datetime.strptime(
        date_string,
        "%Y%m%d"
    ).date()