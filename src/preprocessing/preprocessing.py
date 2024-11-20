import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Download NLTK data files (if you haven't already)
nltk.download('punkt')
nltk.download('stopwords')

def read_csv_files(csv_folder):
    """Reads CSV files and extracts text columns."""
    text_data = []
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            filepath = os.path.join(csv_folder, filename)
            df = pd.read_csv(filepath)
            print(f"Reading {filename}:")
            print(df.head())  # Print the first few rows to inspect the structure of the CSV
            # You can select specific columns to extract text from, modify this as needed.
            
            if filename == 'csv1.csv':
                text_data.extend(df[['column1', 'column2']].dropna().values.flatten())
            
            elif filename == 'csv2.csv':
                text_data.extend(df['column1'].dropna().tolist())
    
    return text_data

def lemmatize_tokens(tokenized_data):
    """Lemmatizes tokenized data."""
    lemmatized_data = []
    for tokens in tokenized_data:
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
        lemmatized_data.append(lemmatized_tokens)
    return lemmatized_data

def correct_spelling(text):
    """Correct spelling of a given string using TextBlob."""
    return str(TextBlob(text).correct())

def tokenize_text(text_data):
    """Tokenizes text data after correcting spelling and removing stopwords."""
    stop_words = set(stopwords.words('english'))
    tokenized_data = []
    
    for text in text_data:
        corrected_text = correct_spelling(text)  # Correct spelling
        tokens = word_tokenize(corrected_text.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Filter non-alphanumeric tokens and stopwords
        tokenized_data.append(filtered_tokens)
    
    return tokenized_data

def tokenize_text_from_csv(csv_file):
    """Tokenizes text from a CSV file."""
    df = pd.read_csv(csv_file)
    text_data = df['productDisplayName'].dropna().tolist()  # Adjust column names as needed
    
    stop_words = set(stopwords.words('english'))
    tokenized_data = []
    
    for text in text_data:
        tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Filter non-alphanumeric tokens and stopwords
        tokenized_data.append(filtered_tokens)
    
    return tokenized_data
