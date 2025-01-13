import json
import os
from collections import defaultdict


def create_barrels_from_inverted_index(input_forward_index_json, output_directory):
    """
    Reads the inverted index and creates barrels based on the first 3 characters of each word.
    Barrels are saved as JSON files where each file contains a dictionary of words and their associated document IDs.

    Parameters:
    - input_forward_index_json: Path to the input JSON file containing the inverted index.
    - output_directory: Directory to save the barrel files.
    """
    try:
        # Ensure the output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Load the inverted index from the JSON file
        print(f"Loading forward index from {input_forward_index_json}...")
        with open(input_forward_index_json, 'r') as json_file:
            forward_index = json.load(json_file)

        # Prepare a dictionary to hold the barrels
        barrels = defaultdict(lambda: defaultdict(list))

        # Iterate through the forward index and group words by their first 3 characters
        print("Partitioning words and creating barrels...")
        for col in forward_index:  # Iterate over columns (like 'gender', 'category', etc.)
            for word in forward_index[col]:
                # Get the first 3 letters of the word (in lowercase)
                word_prefix = word[:3].lower()

                # Only consider words that are at least 3 characters long
                if len(word_prefix) == 3:
                    barrels[word_prefix][word] = forward_index[col][word]

        # Write each barrel file
        for prefix, words in barrels.items():
            # Skip empty barrels
            if len(words) > 0:
                barrel_file = os.path.join(output_directory, f"{prefix}.json")
                print(f"Saving barrel to {barrel_file}...")

                # Save the barrel as a JSON file
                with open(barrel_file, 'w') as json_file:
                    json.dump(words, json_file, indent=4)

        print("Barrels creation complete.")

    except Exception as e:
        print(f"Error: {e}")


# Example usage
input_forward_index_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\Inverted_index_v2.json" # Path to your inverted index JSON file
output_directory = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\abc_alphabetical_barrels"  # Directory to save the barrel files
create_barrels_from_inverted_index(input_forward_index_json, output_directory)
