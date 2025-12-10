#-----VISUALIZATION MODULE-----#
#visualization.py
#-----IMPORTS-----#
from instantiation import st, plt, pd
import numpy as np

#-------------------------------------------------------------------#
#-----DISPLAY-GENERAL-DATASET-INFO-----#
#this function is responsible for displaying general dataset information
#removed function as it is no longer used


#this function displays a histogram of track popularity
def display_track_popularity_histogram(df: pd.DataFrame):
    st.write("<h3 style='text-align:center; font-size:24px'> Distribution of Track Popularity </h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize = (10, 6))
    if "track_popularity" in df.columns:
        df["track_popularity"].hist(bins = 20, ax = ax, color = "#012000", edgecolor = "black")
        ax.set_title("Histogram of Track Popularity")
        ax.set_xlabel("Popularity")
        ax.set_ylabel("Number of Songs")
        st.pyplot(fig)
    else:
        st.info("INFO: No 'track_popularity' column available to plot.")
    st.markdown("-----")


#this function displays a barchart of the average popularity by genre
def display_average_popularity_by_genre(df: pd.DataFrame):
    st.write("<h3 style='text-align:center; font-size:24px'> Average Popularity by Genre </h3>", unsafe_allow_html=True)
    if "playlist_genre" not in df.columns or "track_popularity" not in df.columns:
        st.info("INFO: Required columns for 'Average Popularity by Genre' are missing.")
        return
    avg_popularity = (
        df.groupby("playlist_genre")["track_popularity"]
        .mean()
        .sort_values(ascending = False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize = (10, 5.91))
    ax.bar(avg_popularity.index, avg_popularity.values, color = "#012000")
    ax.set_xlabel("Playlist Genre")
    ax.set_ylabel("Average Popularity")
    plt.xticks(rotation = 45, ha = 'right')
    st.pyplot(fig)
    st.markdown("-----")


#this function is merged from the original calculate_averages_and_create_viz.py file
def display_selected_averages(df: pd.DataFrame, chosen_genre: str, vars_list: list, chosen_subgenre: str = "No Preferred Subgenre"):
    """
    > For each variable in vars_list, we display a bar chart of mean value per playlist_genre and highlight chosen_genre.

    """
    if not vars_list:
        st.info("INFO: No variables chosen to display averages.")
        return

    #create a copy of df with numeric columns of interest; guard for missing columns
    numeric_vars = [v for v in vars_list if v in df.columns]
    if not numeric_vars:
        st.info("INFO: None of the selected variables are available in the dataset.")
        return

    #subset columns that were in the old script
    drop_cols = ['track_name', 'track_artist', 'track_popularity', 'track_album_name', 'playlist_name', 'release_year', 'playlist_subgenre']
    all_values = df.drop(columns = [c for c in drop_cols if c in df.columns], errors = 'ignore')
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    curr_col_num = 0    
    for var in numeric_vars:
        var_values = all_values.groupby('playlist_genre')[var].mean()

        generate_visuals_streamlit(chosen_genre, var, var_values, cols[curr_col_num])
        curr_col_num += 1
    
    if chosen_subgenre != "No Preferred Subgenre":
        curr_col_num = 0
        for var in numeric_vars:
            var_values = df.groupby('playlist_subgenre')[var].mean()
            
            generate_visuals_streamlit(chosen_subgenre, var, var_values, cols[curr_col_num], subgenre=True)
            curr_col_num += 1
            
    st.markdown("-----")

#this function then generates the bar chart 
def generate_visuals_streamlit(genre: str, var: str, values, col, subgenre: bool = False):
    """
    > Plot bar chart where the chosen genre column is highlighted (green to go along with theme) and others are black.

    """
    genre_index = values.index.to_list()
    colors = ["#012000"] * len(genre_index)
    if genre in genre_index:
        colors[genre_index.index(genre)] = '#1DB954'

    min_y = min(values.values)
    max_y = max(values.values)


    fig, ax = plt.subplots()
    #changed this ylim to make sure the lim is never negative
    if var != 'loudness':  #loudness can be negative, so we skip this adjustment
        plt.ylim([min_y - 0.5 * (max_y - min_y) if min_y - 0.5 * (max_y - min_y) > 0 else 0, max_y + 0.25 * (max_y - min_y)])
    else:
        plt.ylim([min_y - 0.5 * (max_y - min_y), max_y + 0.25 * (max_y - min_y)])
    #horizontal line for chosen genre mean (if present)
    if genre in values.index:
        plt.axhline(y = values[genre], color = 'black', linestyle = '--', label = 'Genre Mean')
    ax.bar(genre_index, values.values, color = colors)
    if subgenre:
        ax.set_title(f"Average {var} by Playlist Subgenre")
        ax.set_xlabel("Subgenre")
    else:
        ax.set_title(f"Average {var} by Playlist Genre")
        ax.set_xlabel("Genre")
    ax.set_ylabel(f"Average {var}")
    plt.xticks(rotation = 45, ha = 'right')

    with col:
        st.pyplot(fig)
        if not subgenre:
            st.markdown('----')
        
def generate_comparison_visuals(df: pd.DataFrame, genre: str, selected_features):
    # Plot chart
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_features = df.groupby(genre)[selected_features].mean()
    avg_features.plot(
        kind='bar',
        ax=ax,
        color=["#63E0B0", "#003D17", "#012000"][:len(selected_features)], 
        edgecolor='black'
    )
    plt.xlabel(genre.title())
    plt.title(f'Averages for All Selected Features by {genre.title()}')
    plt.ylabel('Average Value')
    plt.xticks(rotation=45)
    plt.legend(title='Features')
    
    st.pyplot(fig)
        
    
#this function visualizes how the recommended songs compare to the genre average
def plot_recommendation_comparison(recs_df: pd.DataFrame, full_df: pd.DataFrame, genre: str, chosen_vars: list, genre_col: str):
    """
    > Visualizes how the recommended songs compare to the genre average 
      for the specific variables the user selected.
    """
    if not chosen_vars or recs_df.empty:
        return

    # 1. Calculate Averages
    # Avg of the 4(ish) recommended songs
    rec_avg = recs_df[chosen_vars].mean()

    # Avg of the entire genre (the "baseline")
    genre_avg = full_df[full_df[genre_col] == genre][chosen_vars].mean()

    # 2. Prepare Data for Plotting
    labels = [var.title() for var in chosen_vars]
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot two sets of bars
    rects1 = ax.bar(x - width/2, rec_avg, width, label='Your Recs', color='#1DB954') # Spotify Green
    rects2 = ax.bar(x + width/2, genre_avg, width, label=f'Typical {genre.title()}', color='gray', alpha=0.5)
    # Styling
    ax.set_ylabel('Value')
    ax.set_title('Comparison: Your Recs vs. Genre Average')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2)

    # 3. Display
    st.pyplot(fig)
    # 4. (Optional) Text Insight
    # Calculate the biggest difference to give a "smart" insight
    diffs = (rec_avg - genre_avg) / genre_avg * 100
    biggest_change_var = diffs.abs().idxmax()
    change_val = diffs[biggest_change_var]
    
    direction = "higher" if change_val > 0 else "lower"
    st.caption(f"💡 Insight: These recommendations tend to have **{direction} {biggest_change_var}** ({change_val:.1f}%) than the average {genre} song.")
