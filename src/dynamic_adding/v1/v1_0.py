import json
import os
import mmh3
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Initialize NLTK components
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Initialize the MurmurHash3 hash function
def generate_hash(word):
    return mmh3.hash(word)

# Global variable for tracking docid
docid_counter = 59899
def process_and_add_to_barrel(gender, mastercategory, subcategory, year, product_display_name, image_url, barrel_dir):
    global docid_counter

    # Step 1: Tokenize and Lemmatize the product display name
    lemmas = tokenize_and_lemmatize(product_display_name)

    # Step 2: Generate docid once for this product
    current_docid = docid_counter
    docid_counter += 1  # Increment for the next product

    for lemma in lemmas:
        # Step 3: Create barrel file based on the lemma
        barrel_file_path = os.path.join(barrel_dir, f"{lemma[:3].lower()}.json")

        # Step 4: Hash the lemma using MurmurHash
        lemma_hash = generate_hash(lemma)

        # Prepare the data entry to add
        product_entry = f"{current_docid},{product_display_name},{gender},{mastercategory},{subcategory},{year},{image_url},extras"

        # Read or create the JSON file for the lemma barrel
        if os.path.exists(barrel_file_path):
            with open(barrel_file_path, 'r', encoding='utf-8') as file:
                barrel_data = json.load(file)
        else:
            barrel_data = {}  # Create an empty structure if the file doesn't exist

        # Step 5: Add the entry under the correct year in the hash map
        if str(lemma_hash) not in barrel_data:
            barrel_data[str(lemma_hash)] = {}  # Initialize the entry for this lemma hash

        if str(year) not in barrel_data[str(lemma_hash)]:
            barrel_data[str(lemma_hash)][str(year)] = []  # Initialize the year list if it doesn't exist

        # Avoid duplication: Check if product_entry already exists
        if product_entry not in barrel_data[str(lemma_hash)][str(year)]:
            barrel_data[str(lemma_hash)][str(year)].insert(0, product_entry)  # Insert at the top
            print(f"Data for lemma '{lemma}' added to barrel file '{barrel_file_path}' with docid {current_docid}.")
        else:
            print(f"Duplicate entry skipped for lemma '{lemma}' in barrel file '{barrel_file_path}'.")

        # Step 6: Save the updated JSON back to the file
        with open(barrel_file_path, 'w', encoding='utf-8') as file:
            json.dump(barrel_data, file, indent=4)


def tokenize_and_lemmatize(text):
    """Tokenize and lemmatize the given text."""
    tokens = word_tokenize(text)
    # Remove stopwords and punctuations, then lemmatize
    return [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum() and token.lower() not in stop_words]

def process_and_add_to_barrel(gender, mastercategory, subcategory, year, product_display_name, image_url, barrel_dir):
    global docid_counter

    # Step 1: Tokenize and Lemmatize the product display name
    lemmas = tokenize_and_lemmatize(product_display_name)

    for lemma in lemmas:
        # Step 2: Create barrel file based on the lemma
        barrel_file_path = os.path.join(barrel_dir, f"{lemma[:3].lower()}.json")

        # Step 3: Hash the lemma using MurmurHash
        lemma_hash = generate_hash(lemma)

        # Prepare the data entry to add
        product_entry = f"{docid_counter},{product_display_name},{gender},{mastercategory},{subcategory},{year},{image_url},extras"
        docid_counter += 1  # Increment docid for the next entry

        # Read or create the JSON file for the lemma barrel
        if os.path.exists(barrel_file_path):
            with open(barrel_file_path, 'r', encoding='utf-8') as file:
                barrel_data = json.load(file)
        else:
            barrel_data = {}  # Create an empty structure if the file doesn't exist

        # Step 4: Add the entry under the correct year in the hash map
        if str(lemma_hash) not in barrel_data:
            barrel_data[str(lemma_hash)] = {}  # Initialize the entry for this lemma hash

        if str(year) not in barrel_data[str(lemma_hash)]:
            barrel_data[str(lemma_hash)][str(year)] = []  # Initialize the year list if it doesn't exist

        # Avoid duplication: Check if product_entry already exists
        if product_entry not in barrel_data[str(lemma_hash)][str(year)]:
            barrel_data[str(lemma_hash)][str(year)].insert(0, product_entry)  # Insert at the top
            print(f"Data for lemma '{lemma}' added to barrel file '{barrel_file_path}' with docid {docid_counter - 1}.")
        else:
            print(f"Duplicate entry skipped for lemma '{lemma}' in barrel file '{barrel_file_path}'.")

        # Step 5: Save the updated JSON back to the file
        with open(barrel_file_path, 'w', encoding='utf-8') as file:
            json.dump(barrel_data, file, indent=4)


# Example usage
gender = "Boys"
mastercategory = "footwear"
subcategory = "Shoes"
year = 2011
product_display_name = "Nike SB Zoom Blazer Mid"
image_url = "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/a064dc71-61cd-4aa9-a28e-bf9fff7e217b/NIKE+SB+ZOOM+BLAZER+MID.png"
barrel_dir = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\alphabateical_barrels\v4"  # Directory where barrels are stored

process_and_add_to_barrel(gender, mastercategory, subcategory, year, product_display_name, image_url, barrel_dir)
