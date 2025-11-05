#-----VISUALIZATION MODULE-----#
#visualization.py
#-----IMPORTS-----#
from instantiation import st, plt, pd
#-------------------------------------------------------------------#



#this function is responsible for displaying general dataset information
def display_dataset_info(df: pd.DataFrame):

    st.title("Spotify Songs Dataset Visualization")
    
    #display dataset's general information
    st.write("### Preview of the Dataset")
    st.dataframe(df.head())
    
    st.write("### Column Information")
    st.write(df.columns.tolist()) 
    
    st.write("### Summary Statistics")
    st.write(df.describe())
    st.markdown("---")



#this function displays a histogram of track popularity
#⚠️ this function can/should be repurposed to show different data if needed
def display_track_popularity_histogram(df: pd.DataFrame):

    st.write("### Distribution of Track Popularity")
    
    #create the plot using matplotlib
    fig, ax = plt.subplots()
    df["track_popularity"].hist(bins=20, ax=ax, color="skyblue", edgecolor="black")
    ax.set_title("Histogram of Track Popularity")
    ax.set_xlabel("Popularity")
    ax.set_ylabel("Number of Songs")
    
    #display the plot in Streamlit
    st.pyplot(fig)
    st.markdown("---")



#this function displays a barchart of the average popularity by genre
#⚠️ this function can/should be repurposed to show different data if needed
def display_average_popularity_by_genre(df: pd.DataFrame, chart_color: str):
    
    st.write("### Average Popularity by Genre (Top 10)")
    
    avg_popularity = (
        df.groupby("playlist_genre")["track_popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    
    #use st.bar_chart for simplicity, applying the selected color via Matplotlib/Altair 
    #for a more flexible chart would be better, but we'll use st.bar_chart for now.
    #Note: st.bar_chart doesn't have a direct 'color' parameter, but for a simple plot, it's fine.
    #to truly use the selected_color, you'd switch to st.pyplot with a Matplotlib bar chart.
    
    #example using Matplotlib to demonstrate using the selected color
    fig, ax = plt.subplots()
    avg_popularity.plot(kind='bar', ax=ax, color=chart_color) # Apply color here
    ax.set_title("Average Track Popularity by Genre")
    ax.set_xlabel("Playlist Genre")
    ax.set_ylabel("Average Popularity")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("---")