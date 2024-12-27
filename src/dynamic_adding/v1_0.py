import json
import os
import mmh3
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# File to save the current value of docid_counter
DOCID_FILE = "docid_counter.txt"

# Initialize NLTK components
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Initialize the MurmurHash3 hash function
def generate_hash(word):
    return mmh3.hash(word)

# Load or initialize the global docid_counter
if os.path.exists(DOCID_FILE):
    with open(DOCID_FILE, "r") as file:
        docid_counter = int(file.read().strip())
else:
    docid_counter = 610000  # Initialize to 610000 if the file doesn't exist

def save_docid_counter():
    """Save the current value of docid_counter to a file."""
    with open(DOCID_FILE, "w") as file:
        file.write(str(docid_counter))

def tokenize_and_lemmatize(text):
    """Tokenize and lemmatize the given text."""
    tokens = word_tokenize(text)
    # Remove stopwords and punctuations, then lemmatize
    return [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum() and token.lower() not in stop_words]

def process_and_add_to_barrel(gender, mastercategory, subcategory, year, product_display_name, image_url, barrel_dir):
    global docid_counter

    # Step 1: Assign a unique docid for the item
    docid = docid_counter
    docid_counter += 1  # Increment the counter only once for the item

    # Step 2: Save the updated docid_counter to persist its value
    save_docid_counter()

    # Step 3: Tokenize and Lemmatize the product display name
    lemmas = tokenize_and_lemmatize(product_display_name)

    # Step 4: Prepare the product entry
    product_entry = f"{docid},{product_display_name},{gender},{mastercategory},{subcategory},{year},{image_url},extras"

    for lemma in lemmas:
        # Step 5: Create barrel file based on the lemma
        barrel_file_path = os.path.join(barrel_dir, f"{lemma[:3].lower()}.json")

        # Step 6: Hash the lemma using MurmurHash
        lemma_hash = generate_hash(lemma)

        # Read or create the JSON file for the lemma barrel
        if os.path.exists(barrel_file_path):
            with open(barrel_file_path, 'r', encoding='utf-8') as file:
                barrel_data = json.load(file)
        else:
            barrel_data = {}  # Create an empty structure if the file doesn't exist

        # Step 7: Add the entry under the correct year in the hash map
        if str(lemma_hash) not in barrel_data:
            barrel_data[str(lemma_hash)] = {}  # Initialize the entry for this lemma hash

        if str(year) not in barrel_data[str(lemma_hash)]:
            barrel_data[str(lemma_hash)][str(year)] = []  # Initialize the year list if it doesn't exist

        barrel_data[str(lemma_hash)][str(year)].insert(0, product_entry)  # Insert at the top

        # Step 8: Save the updated JSON back to the file
        with open(barrel_file_path, 'w', encoding='utf-8') as file:
            json.dump(barrel_data, file, indent=4)

        print(f"Data for lemma '{lemma}' added to barrel file '{barrel_file_path}' with docid {docid}.")
