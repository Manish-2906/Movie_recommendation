import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    # Correct API call with formatted URL
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f0e439ca177896bfb9f94f05a5735b4e"
    )
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return [], []

# Data load
try:
    movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open("similarity.pkl", "rb"))
except FileNotFoundError as e:
    st.error("Required files are missing. Please ensure 'movie_dict.pkl' and 'similarity.pkl' are available.")
    st.stop()

# Streamlit app
st.title("Movie Recommendation System")

# Dropdown to select a movie
selected_movie_name = st.selectbox("Enter the name of a movie", movies["title"].values)

# Button to show recommendations
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    if names and posters:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            st.image(posters[0])

        with col2:
            st.text(names[1])
            st.image(posters[1])

        with col3:
            st.text(names[2])
            st.image(posters[2])

        with col4:
            st.text(names[3])
            st.image(posters[3])

        with col5:
            st.text(names[4])
            st.image(posters[4])
