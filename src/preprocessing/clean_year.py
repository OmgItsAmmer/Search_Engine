import csv
import re

def clean_year_column(input_csv, output_csv):
    # Regular expression to match valid years (4-digit numbers)
    valid_year_regex = re.compile(r'^\d{4}$')

    # Increase the field size limit if necessary
    csv.field_size_limit(1000000)  # Set a higher limit if needed

    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read and write the header
        header = next(reader)
        writer.writerow(header)

        # Process each row
        for row in reader:
            year = row[1].strip()  # Assuming 2nd column is at index 1
            if not valid_year_regex.match(year):
                row[1] = '0000'  # Replace invalid year with 0000
            writer.writerow(row)

    print(f"Processed CSV saved to {output_csv}")


# Example usage
input_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v3\year_based_hashed_inverted_index.csv"
output_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\inverted_index\v3\cleaned_year_based_hashed_inverted_index.csv"

clean_year_column(input_csv, output_csv)
