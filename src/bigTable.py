import json
import pandas as pd

# Path to the barrels.json file
barrels_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\abc_alphabetical_barrels\age.json"


# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Convert the JSON data into a tabular format
def json_to_table(json_data):
    rows = []

    for category, values in json_data.items():
        for value in values:
            rows.append({"Category": category, "Value": value})

    return pd.DataFrame(rows)


# Save the table to a CSV file (optional)
def save_table(df, output_path):
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Load the barrels.json file
    barrels_data = load_json(barrels_file)

    # Convert JSON to table format
    table = json_to_table(barrels_data)

    # Print the table
    print(table.head())

    # Optional: Save the table to a CSV file
    save_table(table, 'barrels_table.csv')
