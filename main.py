#-----PROGRAM CORE: MAIN-----#
#main.py
#-----IMPORTS-----#
from ui_controls import apply_global_theme
from instantiation import st, initialize_session_state

#-------------------------------------------------------------------#
initialize_session_state()
apply_global_theme()

dashboard = st.Page("pages/Dashboard.py", title='Dashboard')
test = st.Page("pages/Analytics.py", title='Your Analytics')

pg=st.navigation(
    [dashboard, test]
)

pg.run()