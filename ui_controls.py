import streamlit as st

#function that applies the global UI
def apply_global_theme():
    st.markdown("""
        <style>

        /*-----EXPAND-SCROLLABLE-AREA-----*/
        .block-container {
            max-width: 95% !important;
            padding-top: 2rem !important;
        }

        html, body, .stApp {
            height: 100%;
            overflow-y: auto !important;
        }
        /*---------------------------------*/
                


        /*-----BACKGROUND-IMAGE-----*/
        .stApp {
            background: url('https://images.unsplash.com/photo-1483347756197-71ef80e95f73?ixlib=rb-1.2.1&q=85&fm=jpg&w=3840&fit=max') 
                no-repeat center center fixed !important;
            background-size: cover !important;
        }
        /*---------------------------------*/


        /*-----BLUR-AND-TINT-----*/
        .blur-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            backdrop-filter: blur(10px);
            background: rgba(0, 20, 0, 0.55);
            z-index: 0;
        }
        .main > div {
            position: relative;
            z-index: 1;
        }
        /*---------------------------------*/


        /*-----GENERAL-TEXT-COLOR-----*/
        h1, h2, h3, label, p, span, div {
            color: #eaffea !important;
        }
        /*---------------------------------*/


        /*-----SIDEBAR-THEME-----*/
        section[data-testid="stSidebar"] {
            background-color: rgba(5, 20, 5, 0.88) !important;
            backdrop-filter: blur(8px);
            border-right: 1px solid rgba(0,120,0,0.4);
        }

        section[data-testid="stSidebar"] * {
            color: #eaffea !important;
        }
        /*---------------------------------*/


        /*-----DARK-INPUT-FIELDS-----*/
        input, textarea, div[data-baseweb="input"] {
            background-color: rgba(10, 20, 10, 0.8) !important;
            color: #f6fff6 !important;
            border: 1px solid #1DB954 !important;
        }
        /*---------------------------------*/

        /*-----SELECTBOX-DROPDOWN-INPUT-AREA-----*/
        .stSelectbox > div > div {
            background-color: rgba(10, 20, 10, 0.85) !important;
            color: #eaffea !important;
            border: 1px solid #1DB954 !important;
            border-radius: 6px !important;
        }
        /*---------------------------------*/

        /*-----DROP-DOWN-MENU-POPUP-----*/
        ul[role="listbox"] {
            background-color: rgba(5, 15, 5, 0.92) !important;
            color: #eaffea !important;
            border: 1px solid #15883e !important;
        }
        
        /* Dropdown list items */
        li[role="option"] {
            background-color: rgba(10, 20, 10, 0.85) !important;
            color: #eaffea !important;
        }
        li[role="option"]:hover {
            background-color: rgba(20, 40, 20, 0.9) !important;
        }
        /*---------------------------------*/

        /*-----MULTISELECT-FIX-----*/
        .stMultiSelect div[data-baseweb="tag"] {
            background-color: rgba(0, 80, 0, 0.7) !important;
            color: #eaffea !important;
            border: 1px solid #1DB954 !important;
            border-radius: 5px !important;
        }

        /* Remove red X button color */
        .stMultiSelect button {
            color: #bbffbb !important;
        }
        /*---------------------------------*/

        /*-----BUTTON-STYLE-----*/
        .stButton>button {
            background-color: #1DB954 !important;
            color: black !important;
            padding: 0.5rem 1rem !important;
            border-radius: 8px !important;
            font-weight: bold !important;
        }
        .stButton>button:hover {
            background-color: #17a547 !important;
        }

        </style>

        <div class="blur-overlay"></div>
    """, unsafe_allow_html=True)
