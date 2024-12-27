import json
import os
import mmh3
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify, render_template
from src.dynamic_adding.v1_0 import process_and_add_to_barrel

# Initialize the Flask app
app = Flask(__name__)

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Path to barrel directory
BARREL_DIRECTORY = r"F:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\v4barrel\v4"  # Adjust this path to your actual data location

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

def rank_documents(query, documents):
    """Rank documents based on the relevance of the query to the title and remove duplicates."""
    query_lower = query.lower()
    ranked_docs = []
    seen_docs = set()  # Set to track unique document entries based on their content

    for doc in documents:
        # Create a unique identifier for the document based on its fields
        doc_signature = f"{doc['id']}-{doc['title']}-{doc['gender']}-{doc['sub_category']}-{doc['year']}-{doc['image']}"

        if doc_signature in seen_docs:
            continue  # Skip duplicates

        title_lower = doc['title'].lower()
        if query_lower in title_lower:  # Exact match gets highest priority
            rank = 1
        elif all(word in title_lower for word in query_lower.split()):  # Partial match with all words
            rank = 2
        elif any(word in title_lower for word in query_lower.split()):  # Partial match with some words
            rank = 3
        else:
            rank = 4  # Least relevant

        ranked_docs.append((rank, doc))
        seen_docs.add(doc_signature)  # Mark this document as seen

    # Sort documents by rank (ascending order) and return
    ranked_docs.sort(key=lambda x: x[0])
    return [doc for _, doc in ranked_docs]



def find_documents(query, barrel_directory):
    """Find document IDs matching the query with optimization and ranking."""
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
    matching_docs = list(intersected_docs) 

    # Parse the results into structured format
    parsed_results = [parse_document_entry(doc) for doc in matching_docs if parse_document_entry(doc)]

    # Rank the parsed results
    ranked_results = rank_documents(query, parsed_results)

    return ranked_results


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
@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get data from the incoming JSON request
        data = request.json  # Expecting JSON input
        
        # Extract necessary fields from the request
        title = data.get('title', '').strip()
        gender = data.get('gender', '').strip()
        mastercategory = data.get('category', '').strip()  # Changed from mastercategory to category
        subcategory = data.get('subCategory', '').strip()  # Changed from subcategory to subCategory
        year = data.get('year')
        image_url = data.get('image_url', '').strip()

        # Check if all necessary fields are present
        if not all([title, gender, mastercategory, subcategory, year, image_url]):
            return jsonify({"message": "Missing required fields", "status": "error"}), 400
        
        # Optional: You can validate the year and image_url formats if needed
        if not isinstance(year, int) or year < 1900 or year > 2100:
            return jsonify({"message": "Invalid year", "status": "error"}), 400
        
        # Process and add the data to the barrel (function call is assumed to be defined)
        process_and_add_to_barrel(gender, mastercategory, subcategory, year, title, image_url, BARREL_DIRECTORY)
        
        # Return success response
        return jsonify({"message": "Data submitted successfully", "status": "success"}), 200
        
    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")  # Or use logging for more advanced logging
        return jsonify({"message": f"An error occurred: {str(e)}", "status": "error"}), 500



if __name__ == '__main__':
    app.run(debug=True)
