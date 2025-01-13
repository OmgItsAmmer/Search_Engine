import pandas as pd
import json

def create_forward_index(processed_csv, output_json):
    """Creates and saves a forward index."""
    try:
        # Read the processed CSV file
        df = pd.read_csv(processed_csv)

        # Create the forward index
        forward_index = {}
        for _, row in df.iterrows():
            forward_index[row['id']] = {
                'lemmas': row['lemmas'],
                'image_url': row['image_url']  # Include the image URL in the forward index
            }

        # Save the forward index to a JSON file
        with open(output_json, 'w') as f:
            json.dump(forward_index, f, indent=4)
        
        print(f"Forward index saved to {output_json}")
        print("Forward index creation successfully completed!")  # Success message
    except Exception as e:
        print(f"Error creating forward index: {e}")

if __name__ == '__main__':
    # Define file paths
    processed_csv = r"E:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\merged_processed.csv"
    forward_index_json = r"E:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\forward_index.json"

    # Create and save the forward index
    create_forward_index(processed_csv, forward_index_json)
