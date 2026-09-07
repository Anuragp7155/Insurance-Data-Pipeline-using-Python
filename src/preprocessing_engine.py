from pathlib import Path
import pandas as pd

from src.utils import extract_file_date
from src.audit_logger import log_preprocess


# ============================================================
# 1. STANDARDIZE NULL VALUES
# ============================================================

def standardize_nulls(df):
    """
    Converts common representations of missing values
    into proper Pandas missing values.
    """

    null_values = [
        "",
        " ",
        "NA",
        "N/A",
        "na",
        "n/a",
        "NULL",
        "null",
        "None",
        "none",
        "-"
    ]

    # Count missing-like values before replacement
    missing_before = (
        df.isna().sum().sum()
    )

    df = df.replace(
        null_values,
        pd.NA
    )

    # Count missing values after replacement
    missing_after = (
        df.isna().sum().sum()
    )

    newly_standardized = (
        missing_after - missing_before
    )

    print(
        "✓ Null values standardized"
    )

    print(
        f"  Values converted to null: "
        f"{newly_standardized}"
    )

    return df


# ============================================================
# 2. TRIM WHITESPACE
# ============================================================

def trim_text_values(df):
    """
    Removes leading and trailing whitespace
    from text columns.
    """

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    total_trimmed = 0

    for column in text_columns:

        # Keep original values for comparison
        original_values = (
            df[column].copy()
        )

        # Convert to string and trim
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        # Count values that changed
        changed_values = (
            original_values.astype("string")
            != df[column]
        )

        total_trimmed += (
            changed_values
            .fillna(False)
            .sum()
        )

    print(
        "✓ Whitespace trimming completed"
    )

    print(
        f"  Values cleaned: {total_trimmed}"
    )

    return df


# ============================================================
# 3. STANDARDIZE CASE
# ============================================================

def standardize_case(df):
    """
    Standardizes case for selected categorical columns.
    """

    case_columns = [
        "Gender",
        "City",
        "Policy_Type",
        "Region"
    ]

    total_changed = 0
    columns_processed = []

    for column in case_columns:

        if column in df.columns:

            # Keep original values
            original_values = (
                df[column].copy()
            )

            # Standardize case
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .str.title()
            )

            # Count changed values
            changed_values = (
                original_values.astype("string")
                != df[column]
            )

            total_changed += (
                changed_values
                .fillna(False)
                .sum()
            )

            columns_processed.append(
                column
            )

    if columns_processed:

        print(
            "✓ Case standardization completed"
        )

        print(
            f"  Columns processed: "
            f"{', '.join(columns_processed)}"
        )

        print(
            f"  Values standardized: "
            f"{total_changed}"
        )

    else:

        print(
            "✓ Case standardization checked"
        )

        print(
            "  No applicable columns found"
        )

    return df


# ============================================================
# 4. REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):
    """
    Removes completely duplicated rows.
    """

    rows_before = len(df)

    df = df.drop_duplicates()

    rows_after = len(df)

    duplicate_count = (
        rows_before - rows_after
    )

    print(
        "✓ Duplicate check completed"
    )

    print(
        f"  Duplicates removed: "
        f"{duplicate_count}"
    )

    return df, duplicate_count


# ============================================================
# 5. CONVERT DATE COLUMNS
# ============================================================

def convert_date_columns(df):
    """
    Converts available date columns into
    Pandas datetime values.
    """

    date_columns = [
        "Claim_Date",
        "Payment_Date",
        "Start_Date"
    ]

    columns_converted = []

    for column in date_columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            columns_converted.append(
                column
            )

    if columns_converted:

        print(
            "✓ Date columns converted"
        )

        print(
            f"  Columns: "
            f"{', '.join(columns_converted)}"
        )

    else:

        print(
            "✓ Date conversion checked"
        )

        print(
            "  No date columns found"
        )

    return df


# ============================================================
# 6. MAIN PREPROCESSING FUNCTION
# ============================================================

def preprocess_file(
    csv_file,
    output_file
):
    """
    Reads a CSV file, performs preprocessing,
    adds audit columns and saves it as Parquet.
    """

    csv_path = Path(csv_file)
    output_path = Path(output_file)

    try:

        # ----------------------------------------------------
        # Check source file
        # ----------------------------------------------------

        if not csv_path.exists():

            raise FileNotFoundError(
                f"CSV file not found: {csv_path}"
            )

        # ----------------------------------------------------
        # Read CSV
        # ----------------------------------------------------

        df = pd.read_csv(
            csv_path
        )

        print()
        print(
            f"Reading file: {csv_path.name}"
        )

        original_row_count = len(df)

        print(
            f"Original rows: "
            f"{original_row_count}"
        )

        print()
        print(
            "--- DATA CLEANING ---"
        )

        # ----------------------------------------------------
        # 1. Trim whitespace
        # ----------------------------------------------------

        df = trim_text_values(
            df
        )

        # ----------------------------------------------------
        # 2. Standardize null values
        # ----------------------------------------------------

        df = standardize_nulls(
            df
        )

        # ----------------------------------------------------
        # 3. Standardize categorical case
        # ----------------------------------------------------

        df = standardize_case(
            df
        )

        # ----------------------------------------------------
        # 4. Remove duplicates
        # ----------------------------------------------------

        df, duplicate_count = (
            remove_duplicates(df)
        )

        # ----------------------------------------------------
        # 5. Convert date columns
        # ----------------------------------------------------

        df = convert_date_columns(
            df
        )

        # ----------------------------------------------------
        # 6. Extract file date
        # ----------------------------------------------------

        file_date = extract_file_date(
            csv_path.name
        )

        # ----------------------------------------------------
        # 7. Add ingestion date
        # ----------------------------------------------------

        df["ingestion_date"] = (
            pd.Timestamp.now().normalize()
        )

        print(
            "✓ ingestion_date added"
        )

        # ----------------------------------------------------
        # 8. Add file date
        # ----------------------------------------------------

        df["file_date"] = pd.Timestamp(
            file_date
        )

        print(
            "✓ file_date added"
        )

        print()
        print(
            "--- CLEANING COMPLETED ---"
        )

        # ----------------------------------------------------
        # Create output directory
        # ----------------------------------------------------

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # Save as Parquet
        # ----------------------------------------------------

        df.to_parquet(
            output_path,
            index=False
        )

        # ----------------------------------------------------
        # Log successful preprocessing
        # ----------------------------------------------------

        log_preprocess(
            file_name=csv_path.name,
            status="SUCCESS",
            row_count=len(df),
            message=(
                f"Preprocessing completed. "
                f"Original rows: {original_row_count}, "
                f"Duplicates removed: {duplicate_count}, "
                f"Final rows: {len(df)}"
            )
        )

        # ----------------------------------------------------
        # Final output information
        # ----------------------------------------------------

        print()
        print(
            f"Saved: {output_path}"
        )

        print(
            f"Final rows: {len(df)}"
        )

        print(
            f"Final columns: {len(df.columns)}"
        )

        return df

    except Exception as error:

        # ----------------------------------------------------
        # Log failed preprocessing
        # ----------------------------------------------------

        log_preprocess(
            file_name=csv_path.name,
            status="FAILED",
            row_count=None,
            message=str(error)
        )

        print()
        print(
            f"Preprocessing failed: {error}"
        )

        raise