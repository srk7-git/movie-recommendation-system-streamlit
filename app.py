import streamlit as st
import pickle
import requests
from difflib import get_close_matches

# Load data
df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# 🔥 IMPORTANT FIX
df['title_lower'] = df['title'].str.lower()

# 🔥 YOUR API KEY
API_KEY = "81e9da89dc6e5c7d239e00d5b4816cdc"

# Fetch poster
def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        data = requests.get(url).json()

        poster_path = data['results'][0]['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommendation
def recommend(movie):
    movie = movie.lower().strip()

    # ✅ Direct match
    if movie in df['title_lower'].values:
        idx = df[df['title_lower'] == movie].index[0]

    else:
        # 🔍 Fuzzy match
        matches = get_close_matches(movie, df['title_lower'].values, n=1, cutoff=0.6)

        if matches:
            st.warning(f"Did you mean: {matches[0].title()} ?")
            movie = matches[0]
            idx = df[df['title_lower'] == movie].index[0]
        else:
            return [], []

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    movies = []
    posters = []

    for i in scores[1:6]:
        title = df['title'][i[0]]
        movies.append((title, round(i[1], 2)))
        posters.append(fetch_poster(title))

    return movies, posters

# UI
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommendation System")
st.markdown("Get similar movies instantly based on content similarity")
st.write("")

# Input
movie_name = st.text_input("Enter a movie name:")
selected_movie = st.selectbox("Or select a movie:", df['title'].values)

# Button
if st.button("Recommend"):

    if movie_name.strip() != "":
        movie_input = movie_name
    else:
        movie_input = selected_movie

    movies, posters = recommend(movie_input)

    if not movies:
        st.error("Movie not found")
    else:
        st.subheader("Top Recommendations")

        cols = st.columns(5)

        for i in range(len(movies)):
            with cols[i]:
                st.image(posters[i])
                st.caption(f"{movies[i][0]} ⭐ {movies[i][1]}")
