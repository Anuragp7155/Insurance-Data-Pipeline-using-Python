from src.preprocessing_engine import preprocess_file


print()
print("==============================")
print("TEST 1 - MISSING FILE")
print("==============================")


missing_file = (
    "data/ingestion/"
    "file_that_does_not_exist.csv"
)

output_file = (
    "data/preprocessed/"
    "test_output.parquet"
)


try:

    preprocess_file(
        missing_file,
        output_file
    )

    print(
        "❌ TEST FAILED"
    )

except FileNotFoundError:

    print(
        "✓ TEST PASSED"
    )

    print(
        "Missing file was correctly detected."
    )



import pandas as pd

from src.preprocessing_engine import remove_duplicates


print()
print("==============================")
print("TEST 2 - DUPLICATE HANDLING")
print("==============================")


test_df = pd.DataFrame(
    {
        "Customer_ID": [
            "C001",
            "C002",
            "C001"
        ],
        "Name": [
            "Alice",
            "Bob",
            "Alice"
        ]
    }
)


cleaned_df, duplicate_count = (
    remove_duplicates(test_df)
)


print(
    f"Original rows: {len(test_df)}"
)

print(
    f"Final rows: {len(cleaned_df)}"
)

print(
    f"Duplicates removed: {duplicate_count}"
)


if duplicate_count == 1:

    print(
        "✓ TEST PASSED"
    )

else:

    print(
        "❌ TEST FAILED"
    )



from src.preprocessing_engine import trim_text_values


print()
print("==============================")
print("TEST 3 - WHITESPACE CLEANING")
print("==============================")


test_df = pd.DataFrame(
    {
        "City": [
            " Mumbai ",
            "Pune",
            " Delhi "
        ]
    }
)


cleaned_df = trim_text_values(
    test_df
)


expected = [
    "Mumbai",
    "Pune",
    "Delhi"
]


actual = (
    cleaned_df["City"]
    .tolist()
)


if actual == expected:

    print(
        "✓ TEST PASSED"
    )

else:

    print(
        "❌ TEST FAILED"
    )

    print(
        "Expected:",
        expected
    )

    print(
        "Actual:",
        actual
    )


from src.preprocessing_engine import standardize_nulls


print()
print("==============================")
print("TEST 4 - NULL STANDARDIZATION")
print("==============================")


test_df = pd.DataFrame(
    {
        "Customer_ID": [
            "C001",
            "NA",
            "NULL",
            "C004"
        ]
    }
)


cleaned_df = standardize_nulls(
    test_df
)


if (
    pd.isna(
        cleaned_df.loc[1, "Customer_ID"]
    )
    and
    pd.isna(
        cleaned_df.loc[2, "Customer_ID"]
    )
):

    print(
        "✓ TEST PASSED"
    )

else:

    print(
        "❌ TEST FAILED"
    )



from src.preprocessing_engine import standardize_case


print()
print("==============================")
print("TEST 5 - CASE STANDARDIZATION")
print("==============================")


test_df = pd.DataFrame(
    {
        "City": [
            "mumbai",
            "MUMBAI",
            "Mumbai"
        ]
    }
)


cleaned_df = standardize_case(
    test_df
)


expected = [
    "Mumbai",
    "Mumbai",
    "Mumbai"
]


actual = (
    cleaned_df["City"]
    .tolist()
)


if actual == expected:

    print(
        "✓ TEST PASSED"
    )

else:

    print(
        "❌ TEST FAILED"
    )