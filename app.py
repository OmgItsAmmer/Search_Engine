import json
import os
import mmh3
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify, render_template

# Initialize the Flask app
app = Flask(__name__)

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Path to barrel directory
BARREL_DIRECTORY = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\alphabateical_barrels\v4"  # Adjust this path to your actual data location

def lemmatize_query(query):
    """Lemmatize and tokenize the query words."""
    tokens = word_tokenize(query)
    lemmatized = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return lemmatized

def get_barrel_key(word):
    """Return the first three letters of the word."""
    return word[:3]

def murmur_hash(word):
    """Return the Murmur hash value of a word."""
    return mmh3.hash(str(word))

def load_barrel(directory, barrel_key):
    """Load the barrel file corresponding to the barrel key."""
    barrel_file = os.path.join(directory, f"{barrel_key}.json")
    if os.path.exists(barrel_file):
        with open(barrel_file, 'r') as file:
            return json.load(file)
    return {}

def parse_document_entry(entry):
    """
    Parse a document entry string into a structured format.
    Example entry: "9726,Indian Terrain Men Arvis Blue Shirts, Men,Apparel,Topwear,2011.0,http://assets.myntassets.com/v1/images/style/properties/45f9ae69b49e93e5c00e67771aae1c5c_images.jpg,extras"
    """
    parts = entry.split(",")  # Split by commas since the barrel entries are comma-separated
    if len(parts) < 7:
        return None

    doc_id = parts[0].strip()
    title = parts[1].strip()  # Title comes after the document ID
    gender_type = parts[2].strip()  # Gender type comes after title
    sub_category = parts[4].strip()  # Sub-category comes after gender
    year = parts[5].strip()  # Year comes after sub-category
    image_url = parts[6].strip()  # Image URL comes after year

    # Return structured data with separate fields
    return {
        "id": doc_id,
        "title": title,
        "gender": gender_type,  # Gender type field
        "sub_category": sub_category,  # Sub-category field
        "year": year,  # Year field
        "image": image_url  # Image URL field
    }

def find_documents(query, barrel_directory):
    """Find document IDs matching the query with optimization."""
    words = lemmatize_query(query)

    # Dictionary to keep track of document frequencies across all query words
    document_frequency = {}
    intersected_docs = set()  # To store documents that match all query words

    # Iterate over lemmatized words to find matching documents
    for word in words:
        barrel_key = get_barrel_key(word)
        barrel = load_barrel(barrel_directory, barrel_key)
        hash_value = str(murmur_hash(word))

        if hash_value in barrel:
            for year_docs in barrel[hash_value].values():
                for doc in year_docs:
                    # Track the frequency of each document across all query words
                    document_frequency[doc] = document_frequency.get(doc, 0) + 1
                    if document_frequency[doc] == len(words):
                        intersected_docs.add(doc)

    # Merge documents from all years, prioritize intersected items
    matching_docs = list(intersected_docs) + [
        doc for doc, freq in document_frequency.items() if doc not in intersected_docs
    ]

    # Parse the results into structured format
    parsed_results = [parse_document_entry(doc) for doc in matching_docs if parse_document_entry(doc)]

    return parsed_results

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests."""
    data = request.json
    query = data.get('query', '')
    results = find_documents(query, BARREL_DIRECTORY)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
