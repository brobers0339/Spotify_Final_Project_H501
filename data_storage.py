#-----DATA STORAGE MODULE-----#
#data_storage.py
#-----IMPORTS-----#
import pandas as pd
import os
from instantiation import st
from dotenv import load_dotenv
#-------------------------------------------------------------------#

load_dotenv()  #load environment variables from .env file if present
url = os.getenv("TARGET_URL")
survey_path = os.getenv("SURVEY_DATA_PATH")

#-----SPOTIFY-DATASET-HANDLING-----#
@st.cache_data
#this function loads the dataset from the given target URL and then caches it for later
def load_data(url: str) -> pd.DataFrame:
    """Load and cache the Spotify dataset."""
    if not url:
        st.error("ERROR: TARGET_URL is not set in the .env file.")
        return pd.DataFrame()

    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"ERROR: Dataset could not be loaded: {e}")
        return pd.DataFrame()



#this function actually retrieves the cached dataset from the previous function
def get_spotify_dataset() -> pd.DataFrame:
    return load_data()



#-----USER-SURVEY-DATA-HANDLING-----#
#loads the preexisting survey data of the user or an empty dataframe
def initialize_survey_data() -> pd.DataFrame:
    #if the path exists to the survey's save location...
    if os.path.exists(survey_path):
        try:
            #try to read it
            return pd.read_csv(survey_path)
        #if reading failed, throw an error 
        except Exception as e:
            st.error(f"ERROR: Failed to load survey data: {e}")
            return pd.DataFrame(columns=["User Name", "Preferred Genre", "Preferred Subgenre"])
    else:
        #if failed to find a path to the file, return an empty dataframe
        return pd.DataFrame(columns=["User Name", "Preferred Genre", "Preferred Subgenre"])



#this function saves the survey data by appending a single survey response to a CSV and updating the session state
def save_survey_response(user_name: str, genre: str, subgenre: str, chosen_vars: list):
    new_entry = pd.DataFrame([{
        "User Name": user_name,
        "Preferred Genre": genre,
        "Preferred Subgenre": subgenre,
        'Chosen Vars': chosen_vars
    }])
    
    st.session_state.survey_data = new_entry
    st.write(st.session_state.survey_data)




#this function returns the latest survey data from session state or a file saved locally
def get_survey_data() -> pd.DataFrame:
    if "survey_data" in st.session_state:
        return st.session_state.survey_data
    else:
        st.session_state.survey_data = initialize_survey_data()
        return st.session_state.survey_data


