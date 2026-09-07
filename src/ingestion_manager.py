from pathlib import Path
import json
import pandas as pd

from src.audit_logger import log_ingestion


# ============================================================
# LOAD CONTROL FILE
# ============================================================

def load_control_file(control_file):
    """
    Reads a JSON control file
    and returns its contents.
    """

    with open(
        control_file,
        "r"
    ) as file:

        control_data = json.load(file)

    return control_data


# ============================================================
# DISCOVER INCOMING FILES
# ============================================================

def discover_files():
    """
    Finds CSV files present in the ingestion folder.

    For every CSV file, it looks for the corresponding
    JSON control file.
    """

    ingestion_dir = Path(
        "data/ingestion"
    )

    control_dir = Path(
        "config/control_files"
    )

    discovered_files = []

    if not ingestion_dir.exists():

        print(
            "Ingestion folder does not exist:"
        )

        print(
            ingestion_dir
        )

        return discovered_files

    csv_files = sorted(
        ingestion_dir.glob("*.csv")
    )

    for csv_file in csv_files:

        control_file = (
            control_dir /
            f"{csv_file.stem}.json"
        )

        if control_file.exists():

            discovered_files.append(
                {
                    "csv_file": csv_file,
                    "control_file": control_file
                }
            )

        else:

            print(
                f"⚠ Control file not found "
                f"for: {csv_file.name}"
            )

    return discovered_files


# ============================================================
# VALIDATE FILE
# ============================================================

def validate_file(
    csv_file,
    control_file
):
    """
    Validates a CSV file against
    its JSON control file.
    """

    csv_path = Path(csv_file)
    control_path = Path(control_file)

    try:

        # --------------------------------
        # 1. Check whether CSV exists
        # --------------------------------

        if not csv_path.exists():

            raise FileNotFoundError(
                f"CSV file not found: {csv_path}"
            )

        # --------------------------------
        # 2. Check whether JSON exists
        # --------------------------------

        if not control_path.exists():

            raise FileNotFoundError(
                f"Control file not found: "
                f"{control_path}"
            )

        # --------------------------------
        # 3. Read control file
        # --------------------------------

        control = load_control_file(
            control_path
        )

        # --------------------------------
        # 4. Get expected values
        # --------------------------------

        expected_file_name = control[
            "file_name"
        ]

        expected_rows = control[
            "expected_rows"
        ]

        expected_columns = control[
            "expected_columns"
        ]

        expected_extension = control[
            "expected_extension"
        ]

        # --------------------------------
        # 5. Validate filename
        # --------------------------------

        if csv_path.name != expected_file_name:

            raise ValueError(
                f"Filename mismatch. "
                f"Expected: {expected_file_name}, "
                f"Received: {csv_path.name}"
            )

        # --------------------------------
        # 6. Validate extension
        # --------------------------------

        if (
            csv_path.suffix.lower()
            != expected_extension.lower()
        ):

            raise ValueError(
                f"Invalid file extension. "
                f"Expected: {expected_extension}, "
                f"Received: {csv_path.suffix}"
            )

        # --------------------------------
        # 7. Read CSV
        # --------------------------------

        df = pd.read_csv(
            csv_path
        )

        # --------------------------------
        # 8. Validate row count
        # --------------------------------

        actual_rows = len(df)

        if actual_rows != expected_rows:

            raise ValueError(
                f"Row count mismatch. "
                f"Expected: {expected_rows}, "
                f"Received: {actual_rows}"
            )

        # --------------------------------
        # 9. Validate columns
        # --------------------------------

        actual_columns = list(
            df.columns
        )

        if actual_columns != expected_columns:

            raise ValueError(
                f"Column mismatch.\n"
                f"Expected: {expected_columns}\n"
                f"Received: {actual_columns}"
            )

        # --------------------------------
        # 10. Successful validation
        # --------------------------------

        log_ingestion(
            file_name=csv_path.name,
            status="SUCCESS",
            row_count=actual_rows,
            message="File validation successful"
        )

        return True, df

    except Exception as error:

        # --------------------------------
        # Validation failed
        # --------------------------------

        log_ingestion(
            file_name=csv_path.name,
            status="FAILED",
            row_count=None,
            message=str(error)
        )

        return False, None