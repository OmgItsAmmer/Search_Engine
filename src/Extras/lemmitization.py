from nltk.stem import WordNetLemmatizer
from tokenization import tokenized_styles

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to lemmatize a list of tokenized strings
def lemmatize_tokens(tokenized_data):
    lemmatized_data = []
    
    # Iterate over each list of tokens
    for tokens in tokenized_data:
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
        lemmatized_data.append(lemmatized_tokens)
    
    return lemmatized_data

# Example tokenized data (List of lists of strings)


# Lemmatize the tokenized data
lemmatized_data = lemmatize_tokens(tokenized_styles)

# Print the lemmatized data
for lemmatized_tokens in lemmatized_data:
    print(lemmatized_tokens)
