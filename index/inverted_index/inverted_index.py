import json
from collections import defaultdict

def create_inverted_index(forward_index_json, inverted_index_json):
    """Creates and saves an inverted index from the forward index."""
    try:
        # Load the forward index from the JSON file
        with open(forward_index_json, 'r') as f:
            forward_index = json.load(f)
        
        # Initialize a defaultdict for the inverted index
        inverted_index = defaultdict(list)
        
        # Populate the inverted index
        for doc_id, metadata in forward_index.items():
            # Convert the lemmas string to a list (assuming it's stored as a string representation of a list)
            lemmas = eval(metadata['lemmas'])  # Use eval to convert the string to a list
            
            for term in lemmas:
                inverted_index[term].append(doc_id)
        
        # Save the inverted index to a JSON file
        with open(inverted_index_json, 'w') as f:
            json.dump(inverted_index, f, indent=4)
        
        print(f"Inverted index saved to {inverted_index_json}")
        print("Inverted index creation successfully completed!")  # Success message
    except Exception as e:
        print(f"Error creating inverted index: {e}")

if __name__ == '__main__':
    # Define file paths
    forward_index_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\forward_index\forward_index.json"
    inverted_index_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\inverted_index.json"
    
    # Create and save the inverted index
    create_inverted_index(forward_index_json, inverted_index_json)
