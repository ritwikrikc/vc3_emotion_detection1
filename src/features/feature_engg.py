import pandas as pd
import numpy as np  
import os
import yaml
from sklearn.feature_extraction.text import CountVectorizer

with open("params.yaml", 'r') as file:
    params = yaml.safe_load(file)

max_features = params['feature_engg']['max_features']

# Load processed train and test data
train_data = pd.read_csv("data/processed/train.csv").dropna(subset=['content'])
test_data = pd.read_csv("data/processed/test.csv").dropna(subset=['content'])

# Extract features and labels from train and test data
X_train = train_data['content'].values
y_train = train_data['sentiment'].values

X_test = test_data['content'].values
y_test = test_data['sentiment'].values

# Apply Bag of Words (CountVectorizer)
vectorizer = CountVectorizer(max_features=max_features)

# Fit the vectorizer on the training data and transform it to feature vectors
X_train_bow = vectorizer.fit_transform(X_train)

# Transform the test data using the same vectorizer (do not fit again)
X_test_bow = vectorizer.transform(X_test)

# Convert the feature vectors to DataFrames for easier handling
train_df = pd.DataFrame(X_train_bow.toarray())
train_df['sentiment'] = y_train

test_df = pd.DataFrame(X_test_bow.toarray())
test_df['sentiment'] = y_test   

# Save the processed feature data to CSV files
os.makedirs("data/interim", exist_ok=True)  # Ensure the directory exists
train_df.to_csv("data/interim/train_bow.csv", index=False)
test_df.to_csv("data/interim/test_bow.csv", index=False)
