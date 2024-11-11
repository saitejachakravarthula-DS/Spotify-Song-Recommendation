import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
CLIENT_ID = "fbdd5011c07d4de6957766f5f8650a57"
CLIENT_SECRET = "1a51b5a8f4144aa8a4f15fd0df8b100c"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to fetch album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image if not found

# Recommendation function
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')

# Load the music data and similarity data
try:
    music = pickle.load(open('df.pkl', 'rb'))  # Adjust the path if needed
    similarity = pickle.load(open('similarity.pkl', 'rb'))  # Ensure this is loaded correctly
    
    # Verify 'song' column in the DataFrame
    if isinstance(music, pd.DataFrame) and 'song' in music.columns:
        music_list = music['song'].values
    else:
        st.error("The 'df.pkl' file does not have a 'song' column. Please check the file format.")
        st.stop()
except FileNotFoundError:
    st.error("The files 'df.pkl' or 'similarity.pkl' were not found. Ensure both are in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the files: {e}")
    st.stop()

# Song selection dropdown
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
