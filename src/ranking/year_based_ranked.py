import csv
import json
import sys
from collections import defaultdict

def process_inverted_index(input_csv, output_csv, output_json):
    # Set a reasonable field size limit
    csv.field_size_limit(10**7)

    # Initialize a hashmap to store terms and their corresponding years and documents
    term_hashmap = defaultdict(lambda: defaultdict(list))

    # Read the input CSV file
    with open(input_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            term = row['Term']  # Corrected field name
            family_data = row['Family'].split('|')  # Corrected field name
            for doc in family_data:
                doc_parts = doc.split(',')  # Split metadata fields
                if len(doc_parts) < 4:
                    continue  # Skip malformed entries

                year_str = doc_parts[3].strip()  # Extract year as string
                try:
                    year = int(float(year_str))  # Convert to integer year
                except ValueError:
                    print(f"Skipping invalid year value: {year_str}")
                    continue  # Skip this entry if year is invalid

                metadata = doc.strip()  # Extract metadata

                # Store the document metadata under the term and year
                term_hashmap[term][year].append(metadata)

    # Sort years in descending order for each term
    sorted_term_hashmap = {
        term: dict(sorted(years.items(), key=lambda item: -item[0]))  # Sort by year (descending)
        for term, years in term_hashmap.items()
    }

    # Write the hashmap data to a new CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['term', 'year', 'documents']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for term, years in sorted_term_hashmap.items():
            for year, docs in years.items():
                writer.writerow({'term': term, 'year': year, 'documents': ' || '.join(docs)})

    # Write the hashmap data to a JSON file
    with open(output_json, 'w') as jsonfile:
        json_data = {
            term: {str(year): docs for year, docs in years.items()}
            for term, years in sorted_term_hashmap.items()
        }
        json.dump(json_data, jsonfile, indent=4)

    print("Processing complete. Data saved to:")
    print(f"- CSV: {output_csv}")
    print(f"- JSON: {output_json}")

# Example usage
input_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v3\cleaned_inverted_index.csv"  # Input file name
output_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v3\year_based_hashed_inverted_index.csv"  # Output CSV file name
output_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v3\year_based_hashed_inverted_index.json"  # Output JSON file name

process_inverted_index(input_csv, output_csv, output_json)
