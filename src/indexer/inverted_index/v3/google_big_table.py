import pandas as pd
import json
from collections import defaultdict
from google.cloud import bigtable
from google.cloud.bigtable import column_family


# Function to build the inverted index and store it in Google Bigtable
def build_inverted_index_and_store_in_bigtable(csv_file, lexicon_file, bigtable_project, bigtable_instance,
                                               bigtable_table):
    # Load the CSV data
    data = pd.read_csv(csv_file)

    # Load the lexicon JSON file
    with open(lexicon_file, 'r') as lex_file:
        lexicon = json.load(lex_file)

    # Initialize the inverted index (using defaultdict to handle missing terms)
    inverted_index = defaultdict(list)

    # Iterate through each row in the DataFrame
    for _, row in data.iterrows():
        doc_id = row['id']

        # Columns to check for terms
        columns_to_search = ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year',
                             'usage']

        # Process the `lemmas` column (ensure it is a list of terms)
        lemmas = row['lemmas']
        if isinstance(lemmas, str):
            lemmas = json.loads(lemmas.replace("'", '"'))  # Ensure it's parsed correctly

        # Combine all terms from the specified columns and lemmas into a set of unique terms
        terms = set()
        terms.update(row[col] for col in columns_to_search if pd.notna(row[col]))  # Add non-null column values
        terms.update(lemmas)  # Add all lemmas from the lemmas column

        # Build the family string for this document
        family = f"{doc_id}: {row['gender']},{row['masterCategory']},{row['subCategory']},{row['year']},extras"

        # Map terms to the inverted index, checking against the lexicon
        for term in terms:
            if term in lexicon:  # Only include terms found in the lexicon
                inverted_index[term].append(family)

    # Now we have an inverted index with terms mapped to document families
    # Now, save this to Bigtable

    # Initialize Bigtable client and table
    client = bigtable.Client(project=bigtable_project, admin=True)
    instance = client.instance(bigtable_instance)
    table = instance.table(bigtable_table)

    # Process each term and store it in Bigtable
    for term, families in inverted_index.items():
        row_key = term.encode('utf-8')  # Row key is the lexicon term

        row = table.row(row_key)

        # Add column families for the term
        family_index = 1
        for family in families:
            doc_id, details = family.split(": ")
            family_column = f"family{family_index}"
            # Store the doc_id and details in the column
            row.set_cell("doc_data", family_column, f"{doc_id} {details}", timestamp=None)
            family_index += 1

        # Save the row to Bigtable
        row.commit()

    print(f"Inverted index has been successfully stored in Bigtable under the table: {bigtable_table}")


# Example usage of the function
csv_file = r"/data/processed_data/barrels/merged_processed.csv" # CSV file with the required columns
lexicon_file = r"/data/processed_data/lexicons/lexicon.json" # Lexicon JSON file
bigtable_project = "your_project_id"
bigtable_instance = "your_instance_id"
bigtable_table = "BigTable"  # Bigtable table name

# Call the function to build the inverted index and store it in Bigtable
build_inverted_index_and_store_in_bigtable(csv_file, lexicon_file, bigtable_project, bigtable_instance, bigtable_table)
