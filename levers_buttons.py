#-----LEVERS_BUTTONS-----#
#levers_buttons.py

#this module doesn't really do anything right now it just messes around with the colors and sliders and other stuff. Consider
#terminating this module and merging it with visualizations

#-----IMPORTS-----#
from instantiation import st, random
#-------------------------------------------------------------------#
#-----FUNCTION DEFS-----#
def get_random_button_type():
    #helper function that gets a random button type for color and then updates the session state
    types = ["primary", "secondary", "tertiary"]
    #we use a random choice and update the session state
    st.session_state.button_color = random.choice(types)

#this function displays all the buttons, sliders, and text input components on the webpage
#it now returns a dict with the interactive choices for use by the main app
def display_doohickies():    
    st.subheader("Interactive Controls")
    
    #basic Buttons
    if st.button("Reset", type="primary"):
        # reset some session state variables (non-destructive)
        st.session_state.user_text = ""
        st.session_state.button_color = "primary"
        st.success("Reset UI controls")

    if st.button("Say hello"):
        st.write("Why hello there")
    else:
        st.write("Goodbye")
    
    if st.button("Aloha", type="tertiary"):
        st.write("Ciao")
    
    st.markdown("---")
    
    #randomly Color-Changing Button
    st.write("### Dynamic Color Button")
    st.button(
        "Change My Color!",
        type=st.session_state.button_color,
        on_click=get_random_button_type
    )
    st.write(f"The current button type is: **{st.session_state.button_color}**")
    
    st.markdown("---")

    #dynamic Text Box Input
    st.write("### Dynamic Text Input")
    user_input = st.text_input(
        "Type something here to see it printed below:", 
        value=st.session_state.get('user_text', ""), # Use session state for persistence
        key='user_text_input' # Key to manage the widget's state
    )
    
    #update session state
    st.session_state.user_text = user_input
    
    #display logic
    if st.session_state.user_text:
        st.write(f"You typed: **{st.session_state.user_text}**")
    else:
        st.write("Start typing to see the magic!")
        
    st.markdown("---")

    #slider to Change Bar Chart Color
    st.write("### Interactive Chart Color Selection")
    color_options = ["#4D7298", "#74A0D6", "#99CCFF", "#00A0B0", "#FF6F61"]
    color_names = ["Steel Blue", "Royal Blue", "Light Blue", "Teal", "Coral"]
    color_index = st.slider(
        "Select a color for the charts:",
        min_value=0,
        max_value=len(color_options) - 1,
        value=0
    )
    selected_color = color_options[color_index]
    st.write(f"Selected Color: **{color_names[color_index]}** ({selected_color})")
    
    st.markdown("---")
    
    #return a dictionary of choices so the main app can use them
    return {
        "chart_color": selected_color,
        "chart_color_name": color_names[color_index],
        "user_text": st.session_state.user_text,
        "button_type": st.session_state.button_color
    }
