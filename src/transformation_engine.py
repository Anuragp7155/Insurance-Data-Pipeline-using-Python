from pathlib import Path
import pandas as pd


def load_preprocessed_data():
    """
    Loads all preprocessed Parquet datasets.
    """

    base_path = Path(
        "data/preprocessed"
    )

    claims = pd.read_parquet(
        base_path / "claims_20250818.parquet"
    )

    policies = pd.read_parquet(
        base_path / "policies_20250818.parquet"
    )

    customers = pd.read_parquet(
        base_path / "customers_20250818.parquet"
    )

    payments = pd.read_parquet(
        base_path / "payments_20250818.parquet"
    )

    return (
        claims,
        policies,
        customers,
        payments
    )


def build_curated():
    """
    Builds the Curated dataset by joining
    Claims, Policies, Customers and Payments.
    """

    (
        claims,
        policies,
        customers,
        payments
    ) = load_preprocessed_data()

    # ---------------------------------------
    # STEP 1: Claims + Policies
    # ---------------------------------------

    curated = claims.merge(
        policies,
        on="Policy_ID",
        how="left",
        suffixes=(
            "_claim",
            "_policy"
        )
    )

    print(
        "After Claims + Policies:",
        len(curated)
    )

    # ---------------------------------------
    # STEP 2: + Customers
    # ---------------------------------------

    curated = curated.merge(
        customers,
        on="Customer_ID",
        how="left",
        suffixes=(
            "",
            "_customer"
        )
    )

    print(
        "After + Customers:",
        len(curated)
    )

    # ---------------------------------------
    # STEP 3: + Payments
    # ---------------------------------------

    curated = curated.merge(
        payments,
        on="Policy_ID",
        how="left",
        suffixes=(
            "",
            "_payment"
        )
    )

    print(
        "After + Payments:",
        len(curated)
    )

    # ---------------------------------------
    # Select required Curated columns
    # ---------------------------------------

    curated = curated[
        [
            "Claim_ID",
            "Policy_ID",
            "Claim_Amount",
            "Claim_Date",
            "Customer_ID",
            "Policy_Type",
            "Premium_Amount",
            "Start_Date",
            "Customer_Name",
            "Gender",
            "Age",
            "City",
            "Payment_ID",
            "Payment_Date",
            "Payment_Amount"
        ]
    ]

    print()
    print("==============================")
    print("CURATED DATASET")
    print("==============================")

    print(
        "Rows:",
        len(curated)
    )

    print(
        "Columns:"
    )

    print(
        curated.columns.tolist()
    )

    return curated


def save_curated(curated):
    """
    Saves the Curated dataset as Parquet.
    """

    output_path = Path(
        "data/curated/claims_enriched.parquet"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    curated.to_parquet(
        output_path,
        index=False
    )

    print()
    print(
        f"Curated file saved to: {output_path}"
    )


if __name__ == "__main__":

    curated_df = build_curated()

    save_curated(
        curated_df
    )