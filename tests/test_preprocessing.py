from src.preprocessing_engine import preprocess_file


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
    print(
        f"PROCESSING: {dataset.upper()}"
    )
    print("==============================")

    csv_file = (
        f"data/ingestion/"
        f"{dataset}_20250818.csv"
    )

    output_file = (
        f"data/preprocessed/"
        f"{dataset}_20250818.parquet"
    )

    df = preprocess_file(
        csv_file,
        output_file
    )

    print(
        f"Completed: {dataset}"
    )

    print(
        f"Rows: {len(df)}"
    )