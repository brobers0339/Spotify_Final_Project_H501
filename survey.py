#-----SURVEY MODULE-----#
#survey.py
#-----IMPORTS-----#
from instantiation import st, pd
from data_storage import save_survey_response, get_survey_data
#-------------------------------------------------------------------#

#displays the user survey and then stores the user input into the data_storage module
def display_user_survey(df: pd.DataFrame):

    st.title("🎵 Spotify User Survey")

    #UI for actually presenting the form options
    with st.form("user_survey_form"):
        user_name = st.text_input("User Name:")

        #extract the genre options from tthe dataset and present as drop down list
        genre_options = sorted(df["playlist_genre"].dropna().unique().tolist())
        selected_genre = st.selectbox("Preferred Genre:", genre_options)

        #do the same for the subgenre options and provide a drop down list
        subgenre_options = sorted(
            df.loc[df["playlist_genre"] == selected_genre, "playlist_subgenre"]
            .dropna()
            .unique()
            .tolist()
        )
        preferred_subgenre = st.selectbox("Preferred Subgenre:", subgenre_options)
        submitted = st.form_submit_button("Submit Survey")

    

    

    #submission logic for storing that survey data into data_storage module
    if submitted:
        if not user_name.strip():
            st.warning("WARNING: User name is a required field.")
        else:
            save_survey_response(user_name, selected_genre, preferred_subgenre)

    if st.button("Reset Survey"):
            st.rerun()


    #optional presentation of stored data from responses submitted by other users
    st.write("### Current Survey Data:")
    survey_df = get_survey_data()
    st.dataframe(survey_df)
