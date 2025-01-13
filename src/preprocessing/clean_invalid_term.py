import pandas as pd
import nltk
import re

# Download the NLTK words corpus (do this once)
nltk.download('words')
from nltk.corpus import words

# Create a set of valid English words
valid_words = set(words.words())


def clean_invalid_terms(csv_file, output_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Print the columns to debug and check the exact name of the 'Term' column
    print("Columns in CSV:", df.columns)

    # Function to check if the term is a valid word or number
    def is_valid_term(term):
        # Skip if the term is a number
        if re.match(r'^\d+$', str(term)):  # Checks if the term consists of only digits
            return True
        # Check if the term is a valid word in the NLTK words corpus (case insensitive)
        if term.lower() in valid_words:
            return True
        return False

    # Check and filter the rows based on valid terms (use the correct column name 'Term')
    df = df[df['Term'].apply(lambda term: is_valid_term(term))]  # Updated column name 'Term'

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, index=False)


# Example usage
csv_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v4\inverted_index.csv"  # Input CSV file path
output_file = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v4\cleaned_inverted_index.csv"  # Output CSV file path

# Call the function to clean the CSV
clean_invalid_terms(csv_file, output_file)
