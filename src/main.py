from pathlib import Path

from src.ingestion_manager import (
    validate_file,
    discover_files
)

from src.preprocessing_engine import (
    preprocess_file
)

from src.transformation_engine import (
    build_curated,
    save_curated
)

from src.semantic_engine import (
    load_curated,
    build_policy_type_kpi,
    build_city_kpi,
    save_semantic
)

from src.retention_manager import (
    archive_file
)


# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

# Keep this FALSE while developing/testing.
# Change to TRUE only for the final production-style run.
ARCHIVE_ENABLED = False


# ============================================================
# STEP 1 - INGESTION & VALIDATION
# ============================================================

def validate_all_files():

    validated_files = []

    print()
    print("========================================")
    print("STEP 1 - FILE VALIDATION")
    print("========================================")

    discovered_files = discover_files()

    if not discovered_files:

        print()
        print(
            "No files found in data/ingestion."
        )

        return validated_files

    for file_info in discovered_files:

        csv_file = Path(
            file_info["csv_file"]
        )

        control_file = Path(
            file_info["control_file"]
        )

        print()
        print(
            f"Validating: {csv_file.name}"
        )

        valid, df = validate_file(
            csv_file,
            control_file
        )

        if valid:

            print(
                f"✓ {csv_file.name} "
                f"validation successful"
            )

            validated_files.append(
                {
                    "csv_file": csv_file,
                    "control_file": control_file
                }
            )

        else:

            print(
                f"✗ {csv_file.name} "
                f"validation failed"
            )

    print()
    print(
        f"Valid files: {len(validated_files)}"
    )

    print(
        f"Discovered files: "
        f"{len(discovered_files)}"
    )

    return validated_files


# ============================================================
# STEP 2 - PREPROCESSING
# ============================================================

def preprocess_all_files(
    validated_files
):

    print()
    print("========================================")
    print("STEP 2 - PREPROCESSING")
    print("========================================")

    for file_info in validated_files:

        csv_file = Path(
            file_info["csv_file"]
        )

        output_file = (
            Path("data/preprocessed")
            /
            f"{csv_file.stem}.parquet"
        )

        print()
        print(
            f"Preprocessing: "
            f"{csv_file.name}"
        )

        preprocess_file(
            str(csv_file),
            str(output_file)
        )

        print(
            f"✓ {csv_file.name} "
            f"preprocessing completed"
        )


# ============================================================
# STEP 3 - CURATED
# ============================================================

def run_curated_layer():

    print()
    print("========================================")
    print("STEP 3 - CURATED")
    print("========================================")

    curated = build_curated()

    save_curated(
        curated
    )

    print(
        "✓ Curated layer completed"
    )


# ============================================================
# STEP 4 - SEMANTIC / KPI
# ============================================================

def run_semantic_layer():

    print()
    print("========================================")
    print("STEP 4 - SEMANTIC / KPI")
    print("========================================")

    curated = load_curated()

    # Prepare claim-level data
    # so payment joins don't duplicate claims.
    from src.semantic_engine import (
        prepare_claim_data
    )

    claim_df = prepare_claim_data(
        curated
    )

    # KPI-1: Policy-wise
    policy_df = build_policy_type_kpi(
        claim_df
    )

    # KPI-2: City-wise
    city_df = build_city_kpi(
        claim_df
    )

    save_semantic(
        policy_df,
        city_df
    )

    print(
        "✓ Semantic / KPI layer completed"
    )


# ============================================================
# STEP 5 - RETENTION
# ============================================================

def run_retention_layer(
    validated_files
):

    print()
    print("========================================")
    print("STEP 5 - RETENTION")
    print("========================================")

    if not ARCHIVE_ENABLED:

        print()
        print(
            "Archive disabled "
            "(development mode)."
        )

        print(
            "Source files will remain "
            "in data/ingestion."
        )

        return

    for file_info in validated_files:

        csv_file = Path(
            file_info["csv_file"]
        )

        print()
        print(
            f"Archiving: "
            f"{csv_file.name}"
        )

        archive_file(
            str(csv_file)
        )

    print()
    print(
        "✓ Retention completed"
    )


# ============================================================
# MASTER PIPELINE
# ============================================================

def run_pipeline():

    print()
    print("========================================")
    print("       INSURANCE DATA PIPELINE")
    print("========================================")

    # --------------------------------------------------------
    # STEP 1 - INGESTION & VALIDATION
    # --------------------------------------------------------

    validated_files = (
        validate_all_files()
    )

    if not validated_files:

        print()
        print(
            "Pipeline stopped."
        )

        print(
            "No valid files were found."
        )

        return

    # --------------------------------------------------------
    # STEP 2 - PREPROCESSING
    # --------------------------------------------------------

    preprocess_all_files(
        validated_files
    )

    # --------------------------------------------------------
    # STEP 3 - CURATED
    # --------------------------------------------------------

    run_curated_layer()

    # --------------------------------------------------------
    # STEP 4 - SEMANTIC / KPI
    # --------------------------------------------------------

    run_semantic_layer()

    # --------------------------------------------------------
    # STEP 5 - RETENTION
    # --------------------------------------------------------

    run_retention_layer(
        validated_files
    )

    # --------------------------------------------------------
    # COMPLETED
    # --------------------------------------------------------

    print()
    print("========================================")
    print("       PIPELINE COMPLETED")
    print("========================================")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_pipeline()