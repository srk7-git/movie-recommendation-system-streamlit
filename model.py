import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load dataset
movies = pd.read_csv("tmdb_5000_movies.csv")

# Select important columns
movies = movies[['id', 'title', 'overview']]

# Handle missing values
movies.dropna(inplace=True)

# Convert text into vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['overview']).toarray()

# Compute similarity
similarity = cosine_similarity(vectors)

# Save files
pickle.dump(movies, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Files generated successfully!")
