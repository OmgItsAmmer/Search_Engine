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

        barrel_data[str(lemma_hash)][str(year)].insert(0, product_entry)  # Insert at the top

        # Step 5: Save the updated JSON back to the file
        with open(barrel_file_path, 'w', encoding='utf-8') as file:
            json.dump(barrel_data, file, indent=4)

        print(f"Data for lemma '{lemma}' added to barrel file '{barrel_file_path}' with docid {docid_counter - 1}.")
