import pandas as pd
import json
from collections import defaultdict
import ast
import numpy as np  # Import numpy directly

def process_forward_index(input_csv, output_forward_index_json):
    """
    Processes a CSV file to generate a forward index.
    Maps each column (treated as a document) to words and their corresponding 'id' (from the first column).
    Converts all words to lowercase before processing.
    Saves the forward index as a JSON file.

    Parameters:
    - input_csv: Path to the input CSV file
    - output_forward_index_json: Path to save the forward index JSON file
    """
    try:
        # Load the input CSV
        print("Loading CSV data...")
        df = pd.read_csv(input_csv)

        # Ensure 'id' column exists
        if 'id' not in df.columns:
            raise ValueError("The CSV file must have an 'id' column as the first column.")

        forward_index = defaultdict(lambda: defaultdict(list))

        # Iterate through each column (excluding 'id') to process words
        for col in df.columns:
            if col == 'id':
                continue
            print(f"Processing column: {col}")
            for idx, row in df[col].dropna().items():
                doc_id = df.loc[idx, 'id']  # Retrieve 'id' for the current row
                if isinstance(doc_id, np.int64):  # Convert to native int if necessary
                    doc_id = int(doc_id)

                if col == 'lemmas':
                    # Handle 'lemmas' column with lists
                    try:
                        lemmas_list = ast.literal_eval(row)
                        if isinstance(lemmas_list, list):
                            lemmas_list = [lemma.lower() for lemma in lemmas_list]
                            for word in lemmas_list:
                                forward_index[col][word].append(doc_id)
                    except Exception as e:
                        print(f"Skipping invalid lemmas entry: {row} | Error: {e}")
                else:
                    # Split text into words and convert to lowercase
                    words = str(row).lower().split()
                    for word in words:
                        forward_index[col][word].append(doc_id)

        # Convert any int64 doc_ids to native int
        for col in forward_index:
            for word in forward_index[col]:
                forward_index[col][word] = [int(doc_id) for doc_id in forward_index[col][word]]

        # Save forward index as JSON
        print("Saving forward index to JSON...")
        with open(output_forward_index_json, 'w') as json_file:
            json.dump(forward_index, json_file, indent=4)

        print("Forward index processing complete.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\merged_processed.csv"  # Replace with your file path
output_forward_index_json = 'Inverted_index_output.json'
process_forward_index(input_csv, output_forward_index_json)
