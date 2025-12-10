from visualization import (
    display_track_popularity_histogram,
    display_average_popularity_by_genre,
    display_selected_averages,
    generate_comparison_visuals
)
from data_storage import get_spotify_dataset
from data_cleaning import clean_spotify_df
from instantiation import st

#-------------------------------------------------------------------#
st.set_page_config(layout="wide")

spotify_songs_dataset = get_spotify_dataset()


if spotify_songs_dataset.empty:
    st.error("ERROR: Spotify dataset could not be loaded.")
    
else:
    if st.session_state.survey_data is not None:
        chosen_genre = st.session_state.survey_data["Preferred Genre"][0]
        chosen_subgenre = st.session_state.survey_data["Preferred Subgenre"][0]
        chosen_vars = st.session_state.survey_data['Chosen Vars'][0]
        user_name = st.session_state.survey_data['User Name'][0]
        st.write(f"<h1 style='text-align:center;'> Welcome, {user_name} to your Analytics Dashboard!  </h1>", unsafe_allow_html=True)
        st.write("<h2> Overall Statistics </h2>", unsafe_allow_html=True)
        st.markdown("-----")
        #clean dataset (this uses the cleaning pipeline that operates on the already downloaded dataframe)
        cleaned_df = clean_spotify_df(spotify_songs_dataset, filter_year = 2015)

        row0_col1, row0_col2 = st.columns(2)
        st.write("<h2> Your Selected Statistics </h2>", unsafe_allow_html=True)
        st.write("<p style=font-size:48px'><i> Click on any of the graphs to enhance the view. </i> </p>", unsafe_allow_html=True)
        # -----VISUALIZATION----- #
        with row0_col1:
            display_track_popularity_histogram(cleaned_df)

        with row0_col2:
            display_average_popularity_by_genre(cleaned_df)
            
        display_selected_averages(cleaned_df, chosen_genre, chosen_vars, chosen_subgenre)
        
        generate_comparison_visuals(cleaned_df, 'playlist_genre', chosen_vars)
    else:
        st.write("No survey data available. Please complete the survey first.")

