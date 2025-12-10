from instantiation import st
from data_storage import get_spotify_dataset
from data_cleaning import clean_spotify_df
from recommendation import get_recommendations
from visualization import plot_recommendation_comparison
from survey import display_user_survey

#-------------------------------------------------------------------#

spotify_songs_dataset = get_spotify_dataset()

#-----DATA CLEANING-----#
if spotify_songs_dataset.empty:
    st.error("ERROR: Spotify dataset could not be loaded.")
else:
    #clean dataset (this uses the cleaning pipeline that operates on the already downloaded dataframe)
    cleaned_df = clean_spotify_df(spotify_songs_dataset, filter_year = 2015)


# -----RECOMMENDATION UI----- #
if st.session_state.survey_data is not None:
    with st.popover("New Survey Submission"):
    #-----USER-SURVEY-----#
        if not spotify_songs_dataset.empty:
            display_user_survey(spotify_songs_dataset)
        else:
            st.warning("WARNING: Spotify dataset couldn't be loaded. Survey may not function.")

    chosen_genre = st.session_state.survey_data["Preferred Genre"][0]
    chosen_subgenre = st.session_state.survey_data["Preferred Subgenre"][0]
    chosen_vars = st.session_state.survey_data['Chosen Vars'][0]
    user_name = st.session_state.survey_data['User Name'][0]
        
    st.markdown(f"<h1 style='text-align: center;'> Welcome {user_name}! </h1>", unsafe_allow_html=True)
    if chosen_subgenre != "No Preferred Subgenre":
        st.markdown(f"<p style='text-align: center;'> Based on your genre selection of <span style='color:red;'><b>{chosen_genre}</b></span> and subgenre selection of <span style='color:red'><b>{chosen_subgenre}</b></span>, here are some recommended tracks for you: </p>", unsafe_allow_html=True)
        reco = get_recommendations(cleaned_df, chosen_subgenre, chosen_vars, genre_col="playlist_subgenre")
    else:
        st.markdown(f"<p style='text-align: center;'> Based on your genre selection of <span style='color:red;'><b>{chosen_genre}</b></span>, here are some recommended tracks for you: </p>", unsafe_allow_html=True)
        reco = get_recommendations(cleaned_df, chosen_genre, chosen_vars, genre_col="playlist_genre")

    st.subheader("Recommended For You")
    st.markdown("---") # Top separator
    
    for index, row in reco.head(4).iterrows():
        # 1. Convert duration to MM:SS
        duration_min = int(row['duration_sec'] // 60)
        duration_sec = int(row['duration_sec'] % 60)
        time_str = f"{duration_min}:{duration_sec:02d}"
        
        # 2. Display using clean Markdown formatting
        # Using headers (###) makes the song title large and bold
        st.markdown(f"### 🎵 {row['track_name']}")
        
        # Using distinct lines for details
        st.markdown(f"""
        **👤 Artist:** {row['track_artist']}  
        **💿 Album:** {row['track_album_name']}  
        **⏱️ Duration:** {time_str}
        """)
        
        # 3. Add a separator line between songs
        st.markdown("---")
        
        
    with st.expander("**Why these songs? (Analysis)**"):
        if chosen_subgenre != "No Preferred Subgenre":
            genre_col = "playlist_subgenre"
            chosen_overall_genre = chosen_subgenre
        else:
            genre_col = "playlist_genre"
            chosen_overall_genre = chosen_genre
            
        plot_recommendation_comparison(
            recs_df=reco,
            full_df=cleaned_df,
            genre=chosen_overall_genre,
            chosen_vars=chosen_vars,
            genre_col=genre_col
        )
else:
    st.write("No survey data available. Please complete the survey first.")
        #-----USER-SURVEY-----#
    if not spotify_songs_dataset.empty:
        display_user_survey(spotify_songs_dataset)
    else:
        st.warning("WARNING: Spotify dataset couldn't be loaded. Survey may not function.")
