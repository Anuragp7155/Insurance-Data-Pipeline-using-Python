# python -m tests.test_logger 
from src.audit_logger import log_ingestion


log_ingestion(
    file_name="test_file.csv",
    status="SUCCESS",
    row_count=100,
    message="Test log entry"
)

print("Logger test completed.")