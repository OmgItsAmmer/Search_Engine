import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

# Download NLTK data files (if you haven't already)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')  # Added this line to download the missing resource

# Function to read CSV files and extract text columns
def read_csv_files(csv_folder):
    text_data = []
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            filepath = os.path.join(csv_folder, filename)
            df = pd.read_csv(filepath)
            print(f"Reading {filename}:")
            print(df.head())  # Print the first few rows to inspect the structure of the CSV
            # You can select specific columns to extract text from, modify this as needed.
            
            # Example: For the first CSV (10 columns), assume 'column1', 'column2' contain text
            if filename == 'csv1.csv':  # Assuming first CSV is named 'csv1.csv'
                text_data.extend(df[['column1', 'column2']].dropna().values.flatten())
            
            # Example: For the second CSV (2 columns), assume 'column1' contains text
            elif filename == 'csv2.csv':  # Assuming second CSV is named 'csv2.csv'
                text_data.extend(df['column1'].dropna().tolist())

    return text_data

# Tokenize and remove stopwords
def tokenize_text(text_data):
    stop_words = set(stopwords.words('english'))
    tokenized_data = []
    
    for text in text_data:
        tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Filter out non-alphanumeric tokens and stopwords
        tokenized_data.append(filtered_tokens)
    
    return tokenized_data


def tokenize_text_from_csv(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Extract text column(s) to tokenize (adjust column names as needed)
    text_data = df['productDisplayName'].dropna().tolist()  # This assumes 'productDisplayName' contains the text
    
    # Tokenize text
    stop_words = set(stopwords.words('english'))
    tokenized_data = []
    
    for text in text_data:
        tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Filter out non-alphanumeric tokens and stopwords
        tokenized_data.append(filtered_tokens)
    
    return tokenized_data

# Main function to run the entire process
def main():
    # Define your folder path containing the CSV files
    csv_folder = r"C:\Users\ammer\OneDrive\Desktop\Extracted_data\fashion-dataset\csv_folder"
    styles_csv_path = r"C:\Users\ammer\OneDrive\Desktop\Extracted_data\fashion-dataset\csv_folder\styles_new.csv"

    # Example: Tokenize the text from 'styles_new.csv'
    tokenized_styles = tokenize_text_from_csv(styles_csv_path)

    # Print tokenized results
    for tokens in tokenized_styles:
        print(tokens)

if __name__ == '__main__':
    main()
