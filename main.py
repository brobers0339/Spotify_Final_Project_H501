#-----PROGRAM CORE: MAIN-----#
#main.py
#-----IMPORTS-----#
from instantiation import st, initialize_session_state
#-------------------------------------------------------------------#
initialize_session_state()

dashboard = st.Page("pages/Dashboard.py", title='Dashboard')
test = st.Page("pages/Analytics.py", title='Your Analytics')

pg=st.navigation(
    [dashboard, test]
)

pg.run()
