import pandas as pd

# Load the two CSV files into pandas DataFrames
csv1_path = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\merged_processed\merged_processed.csv"
csv2_path = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\raw_data\fashion-dataset\csv_folder\images.csv"

df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

# Remove the '.jpg' extension from the 'filename' column in csv2
df2['filename'] = df2['filename'].str.replace('.jpg', '')

# Convert both 'id' and 'filename' columns to strings for merging
df1['id'] = df1['id'].astype(str)
df2['filename'] = df2['filename'].astype(str)

# Merge the two DataFrames on the 'id' and modified 'filename' columns
merged_df = pd.merge(df1, df2, left_on='id', right_on='filename', how='inner')

# Save the merged DataFrame to a new CSV
output_path = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\merged_output.csv"  # Path to save the merged CSV
merged_df.to_csv(output_path, index=False)

print(f"Merged CSV saved to {output_path}")
