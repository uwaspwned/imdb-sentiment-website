import pickle

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

df = pd.read_csv('IMDB Dataset.csv')

X = df['review']
y = df['sentiment'].map({'negative': 0, 'positive': 1})

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

custom_stop_words = list(ENGLISH_STOP_WORDS - {'not', 'no', "don't", "doesn't", "didn't", "won't"})

pipeline = Pipeline([
    ('vect', CountVectorizer(max_features=10000, stop_words=custom_stop_words, ngram_range=(1,2))),
    ('tfidf', TfidfTransformer()),
    ('model', LogisticRegression(C=2.0, random_state=42, max_iter=1000))
])

pipeline.fit(X_train, y_train)

with open('model.pkl', 'wb') as file:
    pickle.dump(pipeline, file)