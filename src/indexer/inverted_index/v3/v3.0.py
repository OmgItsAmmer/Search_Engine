import pandas as pd
import json
from collections import defaultdict

def build_inverted_index(csv_file, lexicon_file, output_json_file, output_csv_file):
    # Load the CSV data
    data = pd.read_csv(csv_file)

    # Load the lexicon JSON
    with open(lexicon_file, 'r') as lex_file:
        lexicon = json.load(lex_file)

    # Initialize the inverted index (using defaultdict to handle missing terms)
    inverted_index = defaultdict(list)

    # Iterate through each row in the DataFrame
    for _, row in data.iterrows():
        doc_id = row['id']

        # Columns to check for terms
        columns_to_search = ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage','productDisplayName','link']

        # Process the `lemmas` column (ensure it is a list of terms)
        lemmas = row['lemmas']
        if isinstance(lemmas, str):
            lemmas = json.loads(lemmas.replace("'", '"'))  # Ensure it's parsed correctly

        # Combine all terms from the specified columns and lemmas into a set of unique terms
        terms = set()
        terms.update(row[col] for col in columns_to_search if pd.notna(row[col]))  # Add non-null column values
        terms.update(lemmas)  # Add all lemmas from the lemmas column

        # Build the family string for this document
        family = f"{doc_id},{row['productDisplayName']}, {row['gender']},{row['masterCategory']},{row['subCategory']},{row['year']},{row['link']},extras"

        # Map terms to the inverted index, checking against the lexicon
        for term in terms:
            if term in lexicon:  # Only include terms found in the lexicon
                inverted_index[term].append(family)

    # Format the inverted index as required (term -> family1: docId family1: gender,masterCategory,subcategory,year,extras | family2...)
    formatted_index = {}
    for term, families in inverted_index.items():
        formatted_index[term] = ' | '.join(families)

    # Save the inverted index to a JSON file
    with open(output_json_file, 'w') as output:
        json.dump(formatted_index, output, indent=4)

    # Create a list to save the inverted index as a CSV
    csv_data = []
    for term, families in formatted_index.items():
        csv_data.append([term, families])

    # Create a DataFrame and save as CSV
    df = pd.DataFrame(csv_data, columns=["Term", "Family"])
    df.to_csv(output_csv_file, index=False)

# Example usage
csv_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\merged_output.csv" # CSV file with the required columns
lexicon_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\lexicons\lexicon.json"  # Lexicon JSON file
output_json_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v4\inverted_index.json"  # Output file for the inverted index (JSON)
output_csv_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v4\inverted_index.csv"  # Output file for the inverted index (CSV)

build_inverted_index(csv_file, lexicon_file, output_json_file, output_csv_file)
