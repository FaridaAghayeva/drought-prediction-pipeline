import pandas as pd

df = pd.read_csv("data/raw/dataset.csv", nrows=100_000)  # sample first
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.isna().mean().sort_values(ascending=False).head(10))