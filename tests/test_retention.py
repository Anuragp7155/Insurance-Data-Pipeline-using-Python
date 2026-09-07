# python -m tests.test_retention
from pathlib import Path

from src.retention_manager import archive_file


# --------------------------------
# Create a temporary test file
# --------------------------------

test_directory = Path(
    "data/ingestion"
)

test_directory.mkdir(
    parents=True,
    exist_ok=True
)


test_file = (
    test_directory /
    "retention_test.csv"
)


test_file.write_text(
    "id,name\n1,Test"
)


print(
    "Test file created:"
)

print(
    test_file
)


# --------------------------------
# Archive the test file
# --------------------------------

destination = archive_file(
    test_file
)


# --------------------------------
# Verify result
# --------------------------------

print()
print(
    "Source exists:",
    test_file.exists()
)

print(
    "Archive exists:",
    destination.exists()
)