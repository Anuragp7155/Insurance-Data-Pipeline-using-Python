from src.utils import extract_file_date


file_name = "claims_20251017.csv"

result = extract_file_date(file_name)

print("File name:", file_name)
print("Extracted date:", result)