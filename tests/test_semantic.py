from src.semantic_engine import (
    load_curated,
    prepare_claim_data,
    build_policy_type_kpi,
    build_city_kpi,
    save_semantic
)


print()
print(
    "========================================"
)

print(
    "SEMANTIC / KPI TEST"
)

print(
    "========================================"
)


# ============================================================
# Load Curated
# ============================================================

curated = load_curated()


# ============================================================
# Prepare claim-level data
# ============================================================

claim_df = prepare_claim_data(
    curated
)


# ============================================================
# KPI-1
# ============================================================

print()
print(
    "=============================="
)

print(
    "KPI-1 - POLICY WISE"
)

print(
    "=============================="
)


policy_df = build_policy_type_kpi(
    claim_df
)


print(
    policy_df.to_string(
        index=False
    )
)


# ============================================================
# KPI-2
# ============================================================

print()
print(
    "=============================="
)

print(
    "KPI-2 - CITY WISE"
)

print(
    "=============================="
)


city_df = build_city_kpi(
    claim_df
)


print(
    city_df.to_string(
        index=False
    )
)


# ============================================================
# Save
# ============================================================

save_semantic(
    policy_df,
    city_df
)


# ============================================================
# Validation
# ============================================================

print()
print(
    "=============================="
)

print(
    "KPI VALIDATION"
)

print(
    "=============================="
)


# Expected Policy Types from KPI workbook
expected_policy_types = {
    "Auto",
    "Health",
    "Home",
    "Life",
    "Travel"
}


actual_policy_types = set(
    policy_df["PolicyType"]
    .dropna()
)


print(
    "Policy types found:",
    actual_policy_types
)


if expected_policy_types == actual_policy_types:

    print(
        "✓ KPI-1 policy categories PASSED"
    )

else:

    print(
        "❌ KPI-1 policy categories FAILED"
    )


# Expected cities from KPI workbook
expected_cities = {
    "Ahmedabad",
    "Bangalore",
    "Chandigarh",
    "Chennai",
    "Delhi",
    "Hyderabad",
    "Jaipur",
    "Kolkata",
    "Mumbai",
    "Pune"
}


actual_cities = set(
    city_df["PolicyType"]
    .dropna()
)


print(
    "Cities found:",
    actual_cities
)


if expected_cities == actual_cities:

    print(
        "✓ KPI-2 city categories PASSED"
    )

else:

    print(
        "❌ KPI-2 city categories FAILED"
    )


# ============================================================
# Final check
# ============================================================

expected_columns = {
    "PolicyType",
    "TotalClaimAmount",
    "TotalClaims"
}


if set(policy_df.columns) == expected_columns:

    print(
        "✓ KPI-1 columns PASSED"
    )

else:

    print(
        "❌ KPI-1 columns FAILED"
    )


if set(city_df.columns) == expected_columns:

    print(
        "✓ KPI-2 columns PASSED"
    )

else:

    print(
        "❌ KPI-2 columns FAILED"
    )