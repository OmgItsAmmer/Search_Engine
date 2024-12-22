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
BARREL_DIRECTORY = r"data/processed_data/v3"  # Adjust this path to your actual data location

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

def find_documents(query, barrel_directory):
    """Find document IDs matching the query."""
    words = lemmatize_query(query)

    # Retrieve barrels and find matching hash values
    result_sets = []
    for word in words:
        barrel_key = get_barrel_key(word)
        barrel = load_barrel(barrel_directory, barrel_key)
        hash_value = str(murmur_hash(word))

        if hash_value in barrel:
            result_sets.append(set(doc for year_docs in barrel[hash_value].values() for doc in year_docs))

    # Take the intersection of all result sets
    if result_sets:
        common_docs = set.intersection(*result_sets)
    else:
        common_docs = set()

    return list(common_docs)


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
