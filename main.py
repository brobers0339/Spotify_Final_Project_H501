#-----PROGRAM CORE: MAIN-----#
#main.py
#-----IMPORTS-----#
from ui_controls import apply_global_theme
from instantiation import st, pd, initialize_session_state
from data_storage import get_spotify_dataset
from survey import display_user_survey
from levers_buttons import display_doohickies
from visualization import (
    display_dataset_info,
    display_track_popularity_histogram,
    display_average_popularity_by_genre,
    display_selected_averages
)
from data_cleaning import clean_spotify_df
from recommendation import get_recommendations
#-------------------------------------------------------------------#

#-----PROGRAM-INITIALIZATION-----#
initialize_session_state()
apply_global_theme()
spotify_songs_dataset = get_spotify_dataset()



#-----USER-SURVEY-----#
if not spotify_songs_dataset.empty:
    display_user_survey(spotify_songs_dataset)
else:
    st.warning("WARNING: Spotify dataset couldn't be loaded. Survey may not function.")

#-----INTERACTIVE-CONTROLS-----#
controls = display_doohickies()
selected_chart_color = controls.get("chart_color", "#41FF1B")

#-----DATA CLEANING-----#
if spotify_songs_dataset.empty:
    st.error("ERROR: Spotify dataset could not be loaded.")
else:
    #clean dataset (this uses the cleaning pipeline that operates on the already downloaded dataframe)
    cleaned_df = clean_spotify_df(spotify_songs_dataset, filter_year = 2015)

    # -----VISUALIZATION----- #
    display_dataset_info(cleaned_df)
    display_track_popularity_histogram(cleaned_df, chart_color=selected_chart_color)
    display_average_popularity_by_genre(cleaned_df, chart_color=selected_chart_color)

    #interactive panel for selecting variables to visualize averages using merged calculate_averages code
    st.sidebar.header("Average-variable Visuals:")
    #present numeric variables available as options
    numeric_candidates = [c for c in cleaned_df.columns if cleaned_df[c].dtype != object and c not in ("release_year",)]
    default_vars = [v for v in ("danceability", "energy", "valence") if v in numeric_candidates]
    chosen_vars = st.sidebar.multiselect("Please choose up to 3 numeric vars to compute averages", options = numeric_candidates, default = default_vars, max_selections=3)
    chosen_genre = st.sidebar.selectbox("Which genre would you like to highlight in the averages?", options = sorted(cleaned_df["playlist_genre"].unique().tolist()))
    if st.sidebar.button("Show averages visuals"):
        display_selected_averages(cleaned_df, chosen_genre, chosen_vars, selected_chart_color)

    # -----RECOMMENDATION UI----- #
    st.sidebar.header("Song Recommendation:")
    genre_col = st.sidebar.radio("Recommend by:", options = ["playlist_genre", "playlist_subgenre"])
    #guard for missing columns
    if genre_col not in cleaned_df.columns:
        st.sidebar.warning(f"WARNING: Column {genre_col} not present in cleaned dataset.")
    else:
        all_genres = sorted(cleaned_df[genre_col].unique().tolist())
        chosen_genre_for_reco = st.sidebar.selectbox("Choose genre to get a recommendation for:", options = all_genres)
        #variable selection for recommendation
        reco_vars_candidates = [v for v in ["danceability", "energy", "valence", "speechiness", "acousticness", "instrumentalness", "liveness", "tempo", "duration_sec"] if v in cleaned_df.columns]
        chosen_vars_for_reco = st.sidebar.multiselect("Please pick up to 3 variables to match on (priority order matters):", options = reco_vars_candidates, default = ["danceability", "valence", "energy"], help = "Please pick the variables that should guide recommendations", max_selections = 3)

        if st.sidebar.button("Get Recommendation!"):
            if not chosen_vars_for_reco:
                st.sidebar.warning("WARNING: Please select at least one variable for recommendations.")
            else:
                rec = get_recommendations(cleaned_df, chosen_genre_for_reco, chosen_vars_for_reco, genre_col)
                if rec is None or rec.empty:
                    st.sidebar.info("INFO: No recommendation could be produced with the given inputs.")
                else:
                    st.write("### Recommendation:")
                    #show the recommended track(s)
                    st.dataframe(rec[["track_name", "track_artist"] + [c for c in rec.columns if c not in ("track_name","track_artist")] ].head(1))

