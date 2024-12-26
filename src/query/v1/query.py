import json
import os
import mmh3
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()


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


def create_barrel_index(directory):
    """Pre-index available barrel files."""
    return {
        os.path.splitext(file)[0]: os.path.join(directory, file)
        for file in os.listdir(directory) if file.endswith('.json')
    }


def load_barrel_from_index(barrel_index, barrel_key):
    """Load barrel using the pre-created index."""
    if barrel_key in barrel_index:
        with open(barrel_index[barrel_key], 'r') as file:
            return json.load(file)
    return {}


def find_documents(query, barrel_directory):
    """Find document IDs matching the query."""
    # Step 1: Create the barrel index at the start
    barrel_index = create_barrel_index(barrel_directory)

    # Step 2: Lemmatize the query
    words = lemmatize_query(query)

    # Step 3: Retrieve barrels and find matching hash values
    result_sets = []
    for word in words:
        barrel_key = get_barrel_key(word)
        barrel = load_barrel_from_index(barrel_index, barrel_key)
        hash_value = str(murmur_hash(word))

        if hash_value in barrel:
            # Collect all documents for the given hash value
            result_sets.append(set(doc for year_docs in barrel[hash_value].values() for doc in year_docs))

    # Step 4: Take the intersection of all result sets
    if result_sets:
        common_docs = set.intersection(*result_sets)
    else:
        common_docs = set()

    # Clear memory after the query
    barrel_index.clear()

    return list(common_docs)


# Example usage
if __name__ == "__main__":
    # Example directory where barrels are stored
    barrel_directory = "path_to_barrel_directory"

    # Example query
    query = "ben 10"

    # Find documents matching the query
    matching_docs = find_documents(query, barrel_directory)
    print("Matching Documents:", matching_docs)


# Usage Example:
# barrel_directory = "path_to_your_barrels"
# query = "ben 10"
# print(find_documents(query, barrel_directory))



#first code

# # v1.py
#
# import json
# import os
# import mmh3
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import word_tokenize
# from collections import defaultdict
#
# # Initialize the lemmatizer
# lemmatizer = WordNetLemmatizer()
#
# def lemmatize_query(query):
#     """Lemmatize and tokenize the query words."""
#     tokens = word_tokenize(query)
#     lemmatized = [lemmatizer.lemmatize(token.lower()) for token in tokens]
#     return lemmatized
#
# def get_barrel_key(word):
#     """Return the first three letters of the word."""
#     return word[:3]
#
# def murmur_hash(word):
#     """Return the Murmur hash value of a word."""
#     return mmh3.hash(str(word))
#
# def load_barrel(directory, barrel_key):
#     """Load the barrel file corresponding to the barrel key."""
#     barrel_file = os.path.join(directory, f"{barrel_key}.json")
#     if os.path.exists(barrel_file):
#         with open(barrel_file, 'r') as file:
#             return json.load(file)
#     return {}
#
# def find_documents(query, barrel_directory):
#     """Find document IDs matching the query."""
#     # Step 1: Lemmatize the query
#     words = lemmatize_query(query)
#
#     # Step 2: Retrieve barrels and find matching hash values
#     result_sets = []
#     for word in words:
#         barrel_key = get_barrel_key(word)
#         barrel = load_barrel(barrel_directory, barrel_key)
#         hash_value = str(murmur_hash(word))
#
#         if hash_value in barrel:
#             # Collect all documents for the given hash value
#             result_sets.append(set(doc for year_docs in barrel[hash_value].values() for doc in year_docs))
#
#     # Step 3: Take the intersection of all result sets
#     if result_sets:
#         common_docs = set.intersection(*result_sets)
#     else:
#         common_docs = set()
#
#     return list(common_docs)
