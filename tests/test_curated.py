from src.transformation_engine import (
    build_curated,
    save_curated
)


# ---------------------------------------
# Build Curated Dataset
# ---------------------------------------

curated = build_curated()


# ---------------------------------------
# Save Curated Dataset
# ---------------------------------------

save_curated(curated)


# ---------------------------------------
# Test Output
# ---------------------------------------

print()
print("==============================")
print("CURATED TEST")
print("==============================")

print(
    "Shape:",
    curated.shape
)

print()
print("Columns:")

print(
    curated.columns.tolist()
)

print()
print("First 5 rows:")

print(
    curated.head()
)

print()
print("Null values:")

print(
    curated.isna().sum()
)

print()
print(
    "Unique Claims:",
    curated["Claim_ID"].nunique()
)