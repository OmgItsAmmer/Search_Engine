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
        corrected_text = correct_spelling(text)  # Correct spelling
        tokens = word_tokenize(corrected_text.lower())  # Tokenize and convert to lowercase
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
    """Creates a lexicon (unique set of words) from lemmatized data."""
    lexicon = set()
    for tokens in lemmatized_data:
        lexicon.update(tokens)
    return lexicon

def merge_with_image_data(text_df, image_csv):
    """Merges text data with image data using a common 'id' column."""
    try:
        # Load image data
        image_df = pd.read_csv(image_csv)

        # Ensure 'id' columns match formats (strip extensions if necessary)
        text_df['id'] = text_df['id'].astype(str).str.replace('.jpg', '', regex=False)
        image_df['id'] = image_df['id'].astype(str).str.replace('.jpg', '', regex=False)

        # Merge text and image data on 'id'
        merged_data = pd.merge(text_df, image_df, on='id', how='left')
        return merged_data
    except Exception as e:
        print(f"Error merging data: {e}")
        return text_df

def save_processed_data(data, output_csv, output_json):
    """Saves processed data to CSV and JSON files."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)

        # Save to CSV
        data.to_csv(output_csv, index=False)
        print(f"Processed data saved to {output_csv}")

        # Save to JSON
        data.to_json(output_json, orient='records', indent=4)
        print(f"Processed data saved to {output_json}")
    except Exception as e:
        print(f"Error saving processed data: {e}")


def process_csv_files(text_csv, image_csv, output_csv, output_json):
    """Processes text and image CSV files and saves the combined data."""
    try:
        # Load the text data
        print("Loading text data...")
        text_df = pd.read_csv(text_csv)

        # Ensure necessary columns exist
        if 'productDisplayName' not in text_df.columns or 'id' not in text_df.columns:
            raise ValueError("Input text CSV must contain 'productDisplayName' and 'id' columns.")

        text_data = text_df['productDisplayName'].dropna().tolist()

        # Tokenize, lemmatize, and process text data
        print("Processing text data...")
        tokenized_data = tokenize_text(text_data)
        lemmatized_data = lemmatize_tokens(tokenized_data)
        lexicon = create_lexicon(lemmatized_data)

        # Add processed data back to the text DataFrame
        text_df['tokens'] = tokenized_data
        text_df['lemmas'] = lemmatized_data

        # Merge with image data
        print("Merging with image data...")
        merged_data = merge_with_image_data(text_df, image_csv)

        # Save processed and merged data
        print("Saving processed data...")
        save_processed_data(merged_data, output_csv, output_json)

        print(f"Total unique words in the lexicon: {len(lexicon)}")
        print(f"Sample lexicon: {list(lexicon)[:20]}")
    except Exception as e:
        print(f"Error processing CSV files: {e}")

if __name__ == '__main__':
    # Define file paths
    text_csv = r"E:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\raw_data\fashion-dataset\csv_folder\styles_new.csv"
    image_csv = r"E:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\raw_data\fashion-dataset\csv_folder\images.csv"
    output_csv = r"E:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\merged_processed.csv"
    output_json = r"E:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\merged_processed.json"

    # Process the input CSV files
    process_csv_files(text_csv, image_csv, output_csv, output_json)
