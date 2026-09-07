from pathlib import Path
import pandas as pd


# ============================================================
# LOAD CURATED DATA
# ============================================================

def load_curated():
    """
    Loads the Curated dataset.
    """

    curated_path = Path(
        "data/curated/claims_enriched.parquet"
    )

    if not curated_path.exists():

        raise FileNotFoundError(
            f"Curated file not found: {curated_path}"
        )

    df = pd.read_parquet(
        curated_path
    )

    print(
        f"Curated data loaded: {len(df)} rows"
    )

    return df


# ============================================================
# PREPARE UNIQUE CLAIM DATA
# ============================================================

def prepare_claim_data(df):
    """
    Creates a claim-level dataset for KPI calculations.

    A claim should be counted only once even if the
    Curated dataset contains multiple payment records
    for the same policy.
    """

    required_columns = [
        "Claim_ID",
        "Claim_Amount",
        "Policy_Type",
        "City"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing columns in Curated dataset: "
            f"{missing_columns}"
        )

    # Keep one record per claim
    claim_df = (
        df[
            [
                "Claim_ID",
                "Claim_Amount",
                "Policy_Type",
                "City"
            ]
        ]
        .drop_duplicates(
            subset=["Claim_ID"]
        )
        .copy()
    )

    print()
    print(
        "Claim-level KPI data prepared"
    )

    print(
        f"  Curated rows: {len(df)}"
    )

    print(
        f"  Unique claims: "
        f"{claim_df['Claim_ID'].nunique()}"
    )

    return claim_df


# ============================================================
# KPI-1 — POLICY-WISE
# ============================================================

def build_policy_type_kpi(df):
    """
    Builds KPI-1:

    Policy-wise:
    - TotalClaimAmount
    - TotalClaims
    """

    result = (
        df.groupby(
            "Policy_Type",
            dropna=False
        )
        .agg(
            TotalClaimAmount=(
                "Claim_Amount",
                "sum"
            ),
            TotalClaims=(
                "Claim_ID",
                "nunique"
            )
        )
        .reset_index()
    )

    # Rename according to KPI Reporting ResultSet
    result = result.rename(
        columns={
            "Policy_Type": "PolicyType"
        }
    )

    # Sort for easier verification
    result = result.sort_values(
        "PolicyType"
    ).reset_index(
        drop=True
    )

    return result


# ============================================================
# KPI-2 — CITY-WISE
# ============================================================

def build_city_kpi(df):
    """
    Builds KPI-2:

    City-wise:
    - TotalClaimAmount
    - TotalClaims
    """

    result = (
        df.groupby(
            "City",
            dropna=False
        )
        .agg(
            TotalClaimAmount=(
                "Claim_Amount",
                "sum"
            ),
            TotalClaims=(
                "Claim_ID",
                "nunique"
            )
        )
        .reset_index()
    )

    # Rename according to KPI Reporting ResultSet
    result = result.rename(
        columns={
            "City": "PolicyType"
        }
    )

    # Sort for easier verification
    result = result.sort_values(
        "PolicyType"
    ).reset_index(
        drop=True
    )

    return result


# ============================================================
# SAVE KPI OUTPUTS
# ============================================================

def save_semantic(
    policy_df,
    city_df
):
    """
    Saves KPI-1 and KPI-2 outputs as Parquet.
    """

    output_dir = Path(
        "data/semantic"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    policy_output = (
        output_dir /
        "PolicyTypeAgg.parquet"
    )

    city_output = (
        output_dir /
        "CityAgg.parquet"
    )

    policy_df.to_parquet(
        policy_output,
        index=False
    )

    city_df.to_parquet(
        city_output,
        index=False
    )

    print()
    print(
        f"Saved: {policy_output}"
    )

    print(
        f"Saved: {city_output}"
    )


# ============================================================
# MAIN SEMANTIC PIPELINE
# ============================================================

def build_semantic():
    """
    Builds both Semantic KPI datasets.
    """

    print()
    print(
        "========================================"
    )

    print(
        "SEMANTIC / KPI LAYER"
    )

    print(
        "========================================"
    )

    # Load Curated data
    curated = load_curated()

    # Prepare claim-level data
    claim_df = prepare_claim_data(
        curated
    )

    # KPI-1
    print()
    print(
        "Building KPI-1: Policy-wise"
    )

    policy_kpi = build_policy_type_kpi(
        claim_df
    )

    print(
        policy_kpi.to_string(
            index=False
        )
    )

    # KPI-2
    print()
    print(
        "Building KPI-2: City-wise"
    )

    city_kpi = build_city_kpi(
        claim_df
    )

    print(
        city_kpi.to_string(
            index=False
        )
    )

    # Save
    save_semantic(
        policy_kpi,
        city_kpi
    )

    print()
    print(
        "✓ Semantic/KPI layer completed"
    )

    return (
        policy_kpi,
        city_kpi
    )


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    build_semantic()