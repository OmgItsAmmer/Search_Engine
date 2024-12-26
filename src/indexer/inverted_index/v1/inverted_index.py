import json
from collections import defaultdict
from math import log

def create_inverted_index(forward_index_json, inverted_index_json):
    """Creates and saves an inverted index with weights from the forward index."""
    try:
        # Load the forward index from the JSON file
        with open(forward_index_json, 'r') as f:
            forward_index = json.load(f)
        
        # Initialize a defaultdict for the inverted index
        term_document_freq = defaultdict(dict)  # To calculate term frequency in each document
        document_count = len(forward_index)  # Total number of documents

        # Step 1: Calculate term frequencies
        for doc_id, metadata in forward_index.items():
            lemmas = eval(metadata['lemmas'])  # Convert the string representation of a list to a list
            term_count = len(lemmas)  # Total terms in the document
            
            # Count frequency of each term in the document
            for term in lemmas:
                if term not in term_document_freq[term]:
                    term_document_freq[term][doc_id] = 0
                term_document_freq[term][doc_id] += 1 / term_count  # Normalize by total terms
        
        # Step 2: Calculate TF-IDF weights
        inverted_index = defaultdict(list)
        for term, doc_freqs in term_document_freq.items():
            df = len(doc_freqs)  # Document frequency: number of documents containing the term
            idf = log(document_count / df)  # Calculate IDF
            
            for doc_id, tf in doc_freqs.items():
                weight = tf * idf  # TF-IDF
                inverted_index[term].append((doc_id, weight))
        
        # Save the inverted index to a JSON file
        with open(inverted_index_json, 'w') as f:
            json.dump(inverted_index, f, indent=4)
        
        print(f"Inverted index with weights saved to {inverted_index_json}")
        print("Inverted index creation successfully completed!")
    except Exception as e:
        print(f"Error creating inverted index: {e}")

if __name__ == '__main__':
    # Define file paths
    forward_index_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\forward_index\forward_index.json"
    inverted_index_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v3\inverted_index2.json"
    
    # Create and save the inverted index
    create_inverted_index(forward_index_json, inverted_index_json)
