import pandas as pd
from pathlib import Path

files = [f for f in Path("./bom").glob("*.csv") if f.name != "merged_bom.csv"]

dfs = []

for f in files:
    df = pd.read_csv(f, dtype=str)

    # Make Qty numeric
    df["Qty"] = df["Qty"].astype(int)

    project = f.stem
    df["Refs"] = df["Refs"].apply(
        lambda s: ",".join(f"{project}:{r.strip()}" for r in s.split(","))
    )

    dfs.append(df)

bom = pd.concat(dfs, ignore_index=True)

print(bom.head())
print(f"{len(bom)} rows loaded")

merged = (
    bom.groupby(["Value", "Footprint", "DNP"], dropna=False)
       .agg(
           Qty=("Qty", "sum"),
           Refs=("Refs", ",".join),
       )
       .reset_index()
)

merged = merged[["Refs", "Value", "Footprint", "Qty", "DNP"]]
merged.to_csv("./bom/merged_bom.csv", index=False)
