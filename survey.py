#-----SURVEY MODULE-----#
#survey.py
#-----IMPORTS-----#
from instantiation import st, pd
from data_storage import save_survey_response, get_survey_data
#-------------------------------------------------------------------#
#-----SURVEY MODULE-----#
#survey.py
#-----IMPORTS-----#
from instantiation import st, pd
from data_storage import save_survey_response, get_spotify_dataset
from data_cleaning import clean_spotify_df
#-------------------------------------------------------------------#
st.set_page_config(page_title='Home')
#displays the user survey and then stores the user input into the data_storage module
def display_user_survey(df: pd.DataFrame):
    spotify_songs_dataset = get_spotify_dataset()
    cleaned_df = clean_spotify_df(spotify_songs_dataset, filter_year = 2015)


    st.title("🎵 Spotify User Survey")

    #extract the genre options from the dataset and present as drop down list
    genre_options = sorted(df["playlist_genre"].dropna().unique().tolist())
    selected_genre = st.selectbox("Preferred Genre:", genre_options, index=None, placeholder='Please select a genre:', key="preferred_genre")

    #do the same for the subgenre options and provide a drop down list
    subgenre_options = sorted(
        df.loc[df["playlist_genre"] == selected_genre, "playlist_subgenre"]
        .dropna()
        .unique()
        .tolist()
    )
    subgenre_options.append("No Preferred Subgenre")  #option for no subgenre
    #UI for actually presenting the form options
    with st.form("user_survey_form"):
        user_name = st.text_input("User Name:", key="user_name")
        if selected_genre is not None or selected_genre != "":
            preferred_subgenre = st.selectbox("Preferred Subgenre:", subgenre_options, index=subgenre_options.index("No Preferred Subgenre"), placeholder='Please select an option', key="preferred_subgenre")
        numeric_candidates = [c for c in cleaned_df.columns if cleaned_df[c].dtype != object and c not in ("release_year", "track_popularity")]
        chosen_vars = st.multiselect("Please choose up to 3 of your most preferred music variables (the first being your most preferred):", options = numeric_candidates, max_selections=3, key="chosen_vars")
        submitted = st.form_submit_button("Submit Survey", key="submit_survey")



    #submission logic for storing that survey data into data_storage module
    if submitted:
        if not user_name.strip():
            st.warning("WARNING: User name is a required field.")
        elif len(chosen_vars) == 0:
            st.warning("WARNING: Please choose at least one music variable.")
        elif selected_genre is None or selected_genre == "":
            st.warning("WARNING: Please select a preferred genre.")
        else:
            save_survey_response(user_name, selected_genre, preferred_subgenre, chosen_vars)
            st.success("Thank you! Your survey response has been recorded.")
            st.switch_page("pages/Dashboard.py")
            
        if st.button("Reset Survey"):
            st.rerun()
    #optional presentation of stored data from responses submitted by other users
    #st.write("### Current Survey Data:")
    #survey_df = get_survey_data()
    #st.dataframe(survey_df)
    
    