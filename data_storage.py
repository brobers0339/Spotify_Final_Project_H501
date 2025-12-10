#-----DATA STORAGE MODULE-----#
#data_storage.py
#-----IMPORTS-----#
import pandas as pd
import os
from instantiation import st
#-------------------------------------------------------------------#



#-----DATASET-URL-----#
TARGET_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
#-----SURVEY-STORAGE-----#
SURVEY_DATA_PATH = "user_survey_data.csv"



#-----SPOTIFY-DATASET-HANDLING-----#
@st.cache_data
#this function loads the dataset from the given target URL and then caches it for later
def load_data(url: str) -> pd.DataFrame:
    #check to see if the dataset was actually loaded or not and throw an error if not
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"ERROR: Dataset could not be loaded: {e}")
        #on failure, return an empty dataframe
        return pd.DataFrame()



#this function actually retrieves the cached dataset from the previous function
def get_spotify_dataset() -> pd.DataFrame:
    return load_data(TARGET_URL)



#-----USER-SURVEY-DATA-HANDLING-----#
#loads the preexisting survey data of the user or an empty dataframe
def initialize_survey_data() -> pd.DataFrame:
    #if the path exists to the survey's save location...
    if os.path.exists(SURVEY_DATA_PATH):
        try:
            #try to read it
            return pd.read_csv(SURVEY_DATA_PATH)
        #if reading failed, throw an error 
        except Exception as e:
            st.error(f"ERROR: Failed to load survey data: {e}")
            return pd.DataFrame(columns=["User Name", "Preferred Genre", "Preferred Subgenre"])
    else:
        #if failed to find a path to the file, return an empty dataframe
        return pd.DataFrame(columns=["User Name", "Preferred Genre", "Preferred Subgenre"])



#this function saves the survey data by appending a single survey response to a CSV and updating the session state
def save_survey_response(user_name: str, genre: str, subgenre: str):
    new_entry = pd.DataFrame([{
        "User Name": user_name,
        "Preferred Genre": genre,
        "Preferred Subgenre": subgenre
    }])

    #ensure that a valid session data frame exists
    if "survey_data" not in st.session_state:
        st.session_state.survey_data = initialize_survey_data()

    #append the new data in session
    st.session_state.survey_data = pd.concat(
        [st.session_state.survey_data, new_entry], ignore_index=True
    )

    #save the file locally
    st.session_state.survey_data.to_csv(SURVEY_DATA_PATH, index=False)
    st.success("✅ Your responses have been saved!")



#this function returns the latest survey data from session state or a file saved locally
def get_survey_data() -> pd.DataFrame:
    if "survey_data" in st.session_state:
        return st.session_state.survey_data
    else:
        st.session_state.survey_data = initialize_survey_data()
        return st.session_state.survey_data
