import pandas as pd

# Read the data from the provided file path
file_path = "GCUS.GCUS"
try:
    df = pd.read_csv(file_path, sep=r"\s+", skipfooter=1, engine="python")
except FileNotFoundError:
    print(f"File '{file_path}' not found. Please provide the correct file path.")

# Save the DataFrame to a CSV file
df.to_csv("standard_data.csv", index=False)

# Print a success message
print("Data successfully converted to standard_data.csv")
