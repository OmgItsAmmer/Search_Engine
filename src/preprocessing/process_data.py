import pandas as pd
import json
from collections import Counter
import ast


def process_lexicons(input_csv, output_lexicon_csv, output_lexicon_json):
    """
    Processes a CSV file to generate lexicons for all columns except IDs.
    Handles the 'lemmas' column which contains lists of items.
    Converts all words to lowercase before generating the lexicon.
    Saves lexicons as a CSV and JSON file.

    Parameters:
    - input_csv: Path to the input CSV file
    - output_lexicon_csv: Path to save the lexicon CSV file
    - output_lexicon_json: Path to save the lexicon JSON file
    """
    try:
        # Load the input CSV
        print("Loading CSV data...")
        df = pd.read_csv(input_csv)

        # Drop ID column if it exists
        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        lexicon_counter = Counter()

        # Iterate through each column to process lexicons
        for col in df.columns:
            print(f"Processing column: {col}")
            for row in df[col].dropna():
                if col == 'lemmas':
                    # Convert string representation of lists to actual lists
                    try:
                        lemmas_list = ast.literal_eval(row)
                        if isinstance(lemmas_list, list):
                            # Convert lemmas to lowercase
                            lemmas_list = [lemma.lower() for lemma in lemmas_list]
                            lexicon_counter.update(lemmas_list)
                    except Exception as e:
                        print(f"Skipping invalid lemmas entry: {row} | Error: {e}")
                else:
                    # Split other columns into words (space-separated) and convert to lowercase
                    words = str(row).lower().split()
                    lexicon_counter.update(words)

        # Save lexicon as CSV
        print("Saving lexicon to CSV...")
        lexicon_df = pd.DataFrame(lexicon_counter.items(), columns=['Word', 'Count'])
        lexicon_df.sort_values(by='Count', ascending=False, inplace=True)
        lexicon_df.to_csv(output_lexicon_csv, index=False)

        # Save lexicon as JSON
        print("Saving lexicon to JSON...")
        with open(output_lexicon_json, 'w') as json_file:
            json.dump(dict(lexicon_counter), json_file, indent=4)

        print("Lexicon processing complete.")
        print(f"Total unique words: {len(lexicon_counter)}")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
input_csv = 'your_input_file.csv'  # Replace with your file path
output_lexicon_csv = 'lexicon_output.csv'
output_lexicon_json = 'lexicon_output.json'
process_lexicons(input_csv, output_lexicon_csv, output_lexicon_json)
