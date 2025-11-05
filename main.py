#-----PROGRAM CORE: MAIN-----#
#main.py
#-----IMPORTS-----#
from instantiation import st, initialize_session_state
from data_storage import get_spotify_dataset
from survey import display_user_survey
from levers_buttons import display_doohickies
from visualization import (
    display_dataset_info,
    display_track_popularity_histogram,
    display_average_popularity_by_genre
)
#-------------------------------------------------------------------#



#-----PROGRAM-INITIALIZATION-----#
#load data and instantiate the initial state of the streamlit app
initialize_session_state()
spotify_songs_dataset = get_spotify_dataset()



#-----USER-SURVEY-----#
#first check to see that the dataset that is pulled in is not empty, then present the user survey
if not spotify_songs_dataset.empty:
    display_user_survey(spotify_songs_dataset)



#-----INTERACTIVE-CONTROLS-----#
#this shows the interactive controls over the chart based off user input
selected_chart_color = display_doohickies()



#-----VISUALIZATION-----#
#ensure the dataset is not empty, then begin triggering the various functions of the visualization module to display the data
if not spotify_songs_dataset.empty:
    display_dataset_info(spotify_songs_dataset)
    display_track_popularity_histogram(spotify_songs_dataset)
    display_average_popularity_by_genre(spotify_songs_dataset, selected_chart_color)
else:
    #if the dataset returns as empty, throw an error
    st.error("ERROR: Spotify dataset could not be loaded.")
