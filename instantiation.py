#-----INSTANTIATION MODULE-----#
#instantiation.py
#---IMPORTS---#
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import random
#-------------------------------------------------------------------#

#expose common libraries used across modules
__all__ = ["pd", "st", "plt", "random", "initialize_session_state"]


#initialize the session state for streamlit
def initialize_session_state():
    """Initializes Streamlit session state variables."""
    #initialize session state for the dynamic button color thingy
    if 'button_color' not in st.session_state:
        st.session_state.button_color = 'primary'
    
    #add other initializations here later if needed
    st.session_state.setdefault('user_text', '')
    st.session_state.setdefault('survey_data', None)
    st.session_state.setdefault('preferred_genre', '')
    st.session_state.setdefault('preferred_subgenre', '')