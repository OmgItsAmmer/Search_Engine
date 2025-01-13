import pandas as pd

from src.utils.string_constants import OMerged_data_csv

# Load the CSV file
data = pd.read_csv(OMerged_data_csv)

# Replace the values in the 'gender' column with the specified mappings
gender_mapping = {
    'men': 1,
    'boys': 1,
    'girls': 2,
    'women': 2,
    'unisex': 3
}

def map_gender(value):
    return gender_mapping.get(value.lower(), 4)

# Apply the mapping
data['gender'] = data['gender'].apply(map_gender)

# Save the updated data back to a new CSV file without removing column names
data.to_csv('updated_file.csv', index=False, header=True)

print("Gender column updated and saved to 'updated_file.csv'")