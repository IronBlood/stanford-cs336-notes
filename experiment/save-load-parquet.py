# from https://www.datacamp.com/tutorial/apache-parquet

import pandas as pd

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}
df = pd.DataFrame(data)

# Write to Parquet file
df.to_parquet("output/data.parquet", engine="pyarrow", index=False)

print("Parquet file written successfully!")

# Read the Parquet file
df = pd.read_parquet("output/data.parquet", engine="pyarrow")

print("Data from Parquet file:")
print(df)
