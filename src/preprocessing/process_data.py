import nltk
import pandas as pd
import os
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def correct_spelling(text):
    """Correct spelling using TextBlob."""
    try:
        return str(TextBlob(text).correct())
    except Exception as e:
        print(f"Error correcting spelling for text: {text}. Error: {e}")
        return text

def tokenize_text(text_data):
    """Tokenizes, cleans, and removes stopwords from text data."""
    stop_words = set(stopwords.words('english'))
    tokenized_data = []

    for text in text_data:
        if pd.isna(text):
            tokenized_data.append([])
            continue
        tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Remove non-alphanumeric tokens and stopwords
        tokenized_data.append(filtered_tokens)

    return tokenized_data

def lemmatize_tokens(tokenized_data):
    """Lemmatizes tokenized data."""
    lemmatized_data = []
    for tokens in tokenized_data:
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
        lemmatized_data.append(lemmatized_tokens)
    return lemmatized_data

def create_lexicon(lemmatized_data):
    """Creates a lexicon with unique 4-digit IDs for each word."""
    lexicon = {}
    current_id = 1000  # Start IDs from 1000

    for tokens in lemmatized_data:
        for word in tokens:
            if word not in lexicon:
                lexicon[word] = current_id
                current_id += 1

    return lexicon

def save_lexicon(lexicon, output_path):
    """Saves the lexicon as a JSON file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(lexicon, f, indent=4)
        print(f"Lexicon saved to {output_path}")
    except Exception as e:
        print(f"Error saving lexicon: {e}")

def replace_words_with_ids(data, lexicon):
    """
    Replaces token words and lemmatized words with their corresponding IDs
    directly in the 'tokens' and 'lemmas' columns.
    """
    updated_data = []
    for row in data:
        tokens_as_ids = [lexicon.get(word, -1) for word in row['tokens']]  # Replace tokens with IDs
        lemmas_as_ids = [lexicon.get(word, -1) for word in row['lemmas']]  # Replace lemmas with IDs
        row['tokens'] = tokens_as_ids
        row['lemmas'] = lemmas_as_ids
        updated_data.append(row)
    return updated_data

def merge_with_image_data(text_df, image_csv):
    """Merges text data with image data using a common 'id' column. 
    If the 'id' doesn't match, fills non-matching columns with NaN."""
    try:
        # Load image data
        image_df = pd.read_csv(image_csv)

        # Align formats for the 'id' column (remove extensions, trim whitespace)
        text_df['id'] = text_df['id'].astype(str).str.strip().str.replace('.jpg', '', regex=False)
        image_df['id'] = image_df['id'].astype(str).str.strip().str.replace('.jpg', '', regex=False)

        # Ensure no duplicated 'id' values in either DataFrame
        image_df = image_df.drop_duplicates(subset='id', keep='first')
        text_df = text_df.drop_duplicates(subset='id', keep='first')

        # Merge text and image data on 'id' with a left join
        merged_data = pd.merge(text_df, image_df, on='id', how='left')

        # Explicitly ensure unmatched IDs in `image_csv` have NaN values
        unmatched_ids = merged_data[merged_data.isnull().any(axis=1)]
        print(f"Unmatched IDs count: {len(unmatched_ids)}")

        print(f"Merged data contains {len(merged_data)} rows with {merged_data['id'].nunique()} unique IDs.")
        return merged_data

    except Exception as e:
        print(f"Error merging data: {e}")
        return text_df



def save_processed_data(data, output_csv, output_json):
    """Saves processed data to CSV and JSON files."""
    try:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)

        # Save to CSV
        data.to_csv(output_csv, index=False)
        print(f"Processed data saved to {output_csv}")

        # Save to JSON
        data.to_json(output_json, orient='records', indent=4)
        print(f"Processed data saved to {output_json}")
    except Exception as e:
        print(f"Error saving processed data: {e}")

def process_csv_files(text_csv, image_csv, output_csv, output_json, lexicon_json):
    """Processes text and image CSV files and saves the combined data."""
    try:
        # Load the text data
        print("Loading text data...")
        text_df = pd.read_csv(text_csv)

        # Ensure necessary columns exist
        if 'productDisplayName' not in text_df.columns or 'id' not in text_df.columns:
            raise ValueError("Input text CSV must contain 'productDisplayName' and 'id' columns.")

        # Preserve original index
        text_df.reset_index(drop=True, inplace=True)

        # Tokenize and lemmatize text data
        print("Processing text data...")
        text_data = text_df['productDisplayName'].fillna("")  # Replace NaNs with empty strings
        tokenized_data = tokenize_text(text_data)
        lemmatized_data = lemmatize_tokens(tokenized_data)

        # Create lexicon
        print("Creating lexicon...")
        lexicon = create_lexicon(lemmatized_data)
        save_lexicon(lexicon, lexicon_json)

        # Replace words with IDs in the tokens and lemmas columns
        print("Replacing words with IDs...")
        text_df['tokens'] = tokenized_data
        text_df['lemmas'] = lemmatized_data

        # Ensure consistent lengths of data for replacement
        updated_data = replace_words_with_ids(text_df.to_dict(orient="records"), lexicon)
        text_df = pd.DataFrame(updated_data)

        # Merge with image data
        print("Merging with image data...")
        merged_data = merge_with_image_data(text_df, image_csv)

        # Save processed and merged data
        print("Saving processed data...")
        save_processed_data(merged_data, output_csv, output_json)

        print(f"Total unique words in the lexicon: {len(lexicon)}")
        print(f"Sample lexicon: {list(lexicon.items())[:10]}")

    except Exception as e:
        print(f"Error processing CSV files: {e}")


if __name__ == '__main__':
    # Define file paths
    text_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\raw_data\fashion-dataset\csv_folder\styles_new.csv"
    image_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\raw_data\fashion-dataset\csv_folder\images.csv"
    output_csv = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\merged_processed\merged_processed.csv"
    output_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\merged_processed\merged_processed.json"
    lexicon_json = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\lexicons\lexicon.json"

    # Process the input CSV files
    process_csv_files(text_csv, image_csv, output_csv, output_json, lexicon_json)
