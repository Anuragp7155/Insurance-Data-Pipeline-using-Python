import pandas as pd

df = pd.read_parquet(
    "data/curated/claims_enriched.parquet"
)

print(df.head())