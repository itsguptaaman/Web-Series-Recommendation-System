import requests
import streamlit as st
import pickle
import pandas as pd

series_dict = pickle.load(open("series_dict.pkl", "rb"))
series = pd.DataFrame(series_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))


def fetch_poster(series_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/tv/{series_id}?api_key=9496ff6a6a5e7c6bfe16648495338ff8&language=en-US")
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    except Exception as e:
        return "https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg"


def recommend(series_name):
    try:
        series_index = series[series["Series_Title"] == series_name].index[0]
        distances = similarity[series_index]
        series_list = sorted(list(enumerate(distances)), reverse=True, key=lambda i: i[1])[1:6]
        recommended_series = []
        recommended_series_posters = []

        for i in series_list:
            series_id = series.iloc[i[0]].Series_Id
            recommended_series.append(series.iloc[i[0]].Series_Title)
            recommended_series_posters.append(fetch_poster(series_id))

        return recommended_series, recommended_series_posters

    except Exception as e:
        movie_index = series[series["Series_Title"] == series_name].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda i: i[1])[1:6]
        recommended_series = []
        for i in movie_list:
            recommended_series.append(series.iloc[i[0]].Series_Title)
        return recommended_series


st.title("Movie Recommender System")
series_name = st.selectbox("Select a movie to get recommendation", series["Series_Title"].values)

if st.button("Get Recommendation"):
    try:
        names, posters = recommend(series_name)
        print(names)
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

    except Exception as e:
        names = recommend(series_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])

        with col2:
            st.text(names[1])

        with col3:
            st.text(names[2])

        with col4:
            st.text(names[3])

        with col5:
            st.text(names[4])

        st.header("Connect to the internet to get more Info!!!")