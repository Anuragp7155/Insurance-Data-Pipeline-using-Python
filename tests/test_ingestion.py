# python -m tests.test_ingestion

from src.ingestion_manager import discover_files


print()
print("==============================")
print("INGESTION FILE DISCOVERY")
print("==============================")


files = discover_files()


for file_info in files:

    print()
    print(
        "CSV:",
        file_info["csv_file"]
    )

    print(
        "CONTROL:",
        file_info["control_file"]
    )


print()
print(
    "Total files discovered:",
    len(files)
)