# python -m tests.test_validation

from src.ingestion_manager import validate_file


datasets = [
    "agents",
    "claims",
    "customers",
    "payments",
    "policies"
]


for dataset in datasets:

    print()
    print("==============================")
    print(f"VALIDATING: {dataset.upper()}")
    print("==============================")

    csv_file = (
        f"data/ingestion/"
        f"{dataset}_20250818.csv"
    )

    control_file = (
        f"config/control_files/"
        f"{dataset}_20250818.json"
    )

    valid, df = validate_file(
        csv_file,
        control_file
    )

    if valid:

        print("STATUS: VALID")
        print("ROWS:", len(df))

    else:

        print("STATUS: INVALID")