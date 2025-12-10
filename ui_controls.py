import streamlit as st

#function that applies the global UI
def apply_global_theme():
    st.markdown("""
        <style>

        /*-----EXPAND-SCROLLABLE-AREA-----*/
        .block-container {
            max-width: 98% !important;
            padding-top: 2rem 1.5rem !important;
        }

        html, body, .stApp {
            height: 100%;
            overflow-y: auto !important;
        }
        /*---------------------------------*/
                


        /*-----BACKGROUND-IMAGE-----*/
        .stApp {
            background: url('https://www.nps.gov/npgallery/GetAsset/98bfa86a-4e3a-4cec-b641-9dccd7377fab/proxy/hires?') 
                no-repeat center center fixed !important;
            background-size: cover !important;
        }
        /*---------------------------------*/


        /*-----BLUR-AND-TINT-----*/
        .blur-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;

            /* Blur applies to everything behind this layer (the background) */
            backdrop-filter: blur(10px);

            /* Tint layer */
            background: rgba(0, 20, 0, 0.55);

            /* KEEP THIS ABOVE THE BACKGROUND BUT BELOW THE UI */
            z-index: -1;

            /* Make sure this layer never blocks clicks */
            pointer-events: none;
        }

        /* Ensure all Streamlit content renders ABOVE the tint */
        .stApp, .stApp > * {
            position: relative;
            z-index: 1 !important;
        }
        
        /*-----GENERAL-TEXT-COLOR-----*/
        h1, h2, h3, label, p, div {
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
        
        /* ----- MATCH MULTISELECT INPUT TO SELECTBOX ----- */
        div[data-baseweb="select"] {
            background-color: rgba(10, 20, 10, 0.85) !important;
            border: 1px solid #1DB954 !important;
            border-radius: 6px !important;
            color: #eaffea !important;
        }

        /* Inside area where selected tags appear */
        div[data-baseweb="select"] > div {
            background-color: rgba(10, 20, 10, 0.85) !important;
        }

        /* Search text inside the multiselect */
        div[data-baseweb="select"] input {
            color: #eaffea !important;
        }

        /* Selected tag styling (you already have this; just keep it) */
        .stMultiSelect div[data-baseweb="tag"] {
            background-color: rgba(0, 80, 0, 0.7) !important;
            color: #eaffea !important;
            border: 1px solid #1DB954 !important;
            border-radius: 5px !important;
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
        <div class="background-layer"></div>
        <div class="blur-overlay"></div>
    """, unsafe_allow_html=True)
