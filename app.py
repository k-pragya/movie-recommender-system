import pandas as pd
import streamlit as st
import requests
import pickle

# CSS with the Base64 encoded image and label styling
background_css = f"""
<style>
    .stApp {{
          background-color:  #023020;
    }}
    /* Styling all labels, including selectbox label */
    div[data-testid="stSidebar"] label, label {{
        color: #FFFFFF !important;  /* Ensure label text is white */
        font-size: 50px !important;  /* Increase font size */
    }}
    h1, h2, h3 {{
        color:  #FFFFFF;  /* Heading color */
    }}
    .stButton>button {{
        width: 40%;
        padding: 12px;
        background-color: #008B8B;
        color: white;
        border-radius: 2px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s;
        border: 5px solid black;
    }}
    .stButton>button:hover {{
        background-color: #FFFFFF;  /* Button hover color */
    }}
</style>
"""

# Inject CSS
st.markdown(background_css, unsafe_allow_html=True)

# Title
st.markdown('<h1 style="text-align: center;">Movie Recommender System</h1>', unsafe_allow_html=True)
# function to fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b2e0a4d14a2304c13f1d8def990fc6a9&language=en-US"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Ensure valid response
        data = response.json()
        poster_path = data.get('poster_path')
        return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

# function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch the movie poster
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


movies1 = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies1)
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select or enter a movie name",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<p style='color:white;'>{recommended_movie_names[0]}</p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[0])
    with col2:
        st.markdown(f"<p style='color:white;'>{recommended_movie_names[1]}</p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[1])

    with col3:
        st.markdown(f"<p style='color:white;'>{recommended_movie_names[2]}</p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[2])
    with col4:
        st.markdown(f"<p style='color:white;'>{recommended_movie_names[3]}</p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[3])
    with col5:
        st.markdown(f"<p style='color:white;'>{recommended_movie_names[4]}</p>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[4])
