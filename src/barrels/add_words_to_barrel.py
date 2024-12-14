import json
import os


def update_or_create_barrel(word_input, output_directory):
    """
    Takes words as input, checks if the corresponding barrel exists, and updates it or creates a new one.
    If the word already exists in the barrel, it notifies the user and does nothing.

    Parameters:
    - word_input: User input (string) containing one or more words.
    - output_directory: Directory where barrel JSON files are stored.
    """
    # Split the input into individual words
    words = word_input.strip().split()

    for word in words:
        # Get the first 3 letters of the word (in lowercase)
        word_prefix = word[:3].lower()

        # Only process words with at least 3 characters
        if len(word_prefix) == 3:
            barrel_file = os.path.join(output_directory, f"{word_prefix}.json")

            # Check if the barrel file exists
            if os.path.exists(barrel_file):
                # Load the existing barrel
                with open(barrel_file, 'r') as json_file:
                    barrel_data = json.load(json_file)

                # If word already exists in the barrel, notify the user
                if word in barrel_data:
                    print(f"'{word}' already exists in '{word_prefix}' barrel. No changes made.")
                else:
                    # Add the word to the barrel
                    barrel_data[word] = []  # Add an empty list of doc IDs (we'll add docs later)
                    with open(barrel_file, 'w') as json_file:
                        json.dump(barrel_data, json_file, indent=4)
                    print(f"'{word}' has been added to the '{word_prefix}' barrel.")

            else:
                # If the barrel doesn't exist, create a new one
                print(f"Creating new barrel for '{word_prefix}'...")

                # Create a new barrel with the word
                barrel_data = {word: []}  # Add the word with an empty doc ID list
                with open(barrel_file, 'w') as json_file:
                    json.dump(barrel_data, json_file, indent=4)
                print(f"'{word}' has been added to the newly created '{word_prefix}' barrel.")


# Example usage
output_directory = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\abc_alphabetical_barrels"  # Directory where barrels are stored

# Example: Prompt the user for input and process it
user_input = input("Enter one or more words: ")
update_or_create_barrel(user_input, output_directory)
