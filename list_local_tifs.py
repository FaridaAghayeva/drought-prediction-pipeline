import re
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")

paths = sorted(list(RAW.rglob("*.tif")) + list(RAW.rglob("*.tiff")))
if not paths:
    raise SystemExit(f"No .tif/.tiff files found under {RAW.resolve()}")

df = pd.DataFrame({"path": [str(p.relative_to(RAW)) for p in paths]})
df["folder"] = [str(p.parent.relative_to(RAW)) or "(top level)" for p in paths]
df["file"] = [p.name for p in paths]
df["size_mb"] = [round(p.stat().st_size / 1e6, 1) for p in paths]
df["sensor"] = df["file"].map(lambda f: f.split("_")[0])


def parse_date(name):
    m = re.search(r"(\d{8})T(\d{6})", name)
    if m:
        return pd.to_datetime(m[1] + m[2], format="%Y%m%d%H%M%S", errors="coerce")
    m = re.search(r"((?:19|20)\d{2})[-_]?(\d{2})[-_]?(\d{2})", name)
    if m:
        return pd.to_datetime(f"{m[1]}-{m[2]}-{m[3]}", errors="coerce")
    return pd.NaT


df["datetime"] = df["file"].map(parse_date)
df["date"] = df["datetime"].dt.date
df = df.sort_values(["folder", "datetime"]).reset_index(drop=True)

print(f"{len(df)} TIFs, {df['size_mb'].sum() / 1000:.1f} GB total\n")
for folder, g in df.groupby("folder"):
    d = g["datetime"].dropna()
    print(f"[{folder}]  {len(g)} files")
    if len(d):
        gaps = d.sort_values().diff().dt.days.dropna()
        print(f"   dates: {d.min().date()} -> {d.max().date()}")
        if len(gaps):
            print(f"   typical gap: {gaps.median():.0f} days (max {gaps.max():.0f})")
    print(f"   sensors: {', '.join(sorted(g['sensor'].unique()))}")
    print(f"   no date parsed: {g['datetime'].isna().sum()}")
    dup = g["date"].duplicated(keep=False) & g["datetime"].notna()
    print(f"   files sharing a date with another file: {dup.sum()}\n")

print(df[["file", "date", "size_mb"]].head(15).to_string(index=False))

Path("docs").mkdir(exist_ok=True)
df.drop(columns=["datetime"]).to_csv("docs/tif_inventory.csv", index=False)
print("\nSaved full list to docs/tif_inventory.csv")
