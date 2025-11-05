def make_recommendation(df, grouped_df, chosen_genre, chosen_var, genre_col):
    '''
    Filter given dataset subset relating to chosen genre based on the chosen variable and it's generated mean value.
    Utilizing a mean range, only retain rows that have a variable value within the calculated range (mean value +/- 10% of the mean value).

    Parameters
    ----------
    df : pandas.DataFrame
      Cleaned dataset generated from clean data module (whenever that is implemented).
    grouped_df : DataFrameGroupBy
      Grouped pandas dataframe based on selected genre_col value, playlist_genre or playlist_subgenre.
    chosen_genre : str
      String containing the user selected genre generated from streamlit input.
    chosen_var : str
      String of current selected var, either amongst the 3 initially user selected variables or 
      an iteration of the rest of the variables depending on the current iteration in the get_recommendations function.
    genre_col : str
      String of selected genre type, resulting in playlist_genre or playlist_subgenre

    Returns
    -------
    filtered_df : pandas.DataFrame
      Filtered dataframe only containing rows that contain values of the chosen variable within the calculated mean of that same variable.

    Notes
    -----
     - Current range is at 10% of the original mean. This was just a value I landed on that seemed to account for the variance in the different values best.
       We can always alter this however we see fit.
       
    '''
    chosen_var_mean_value = grouped_df.get_group(chosen_genre)[chosen_var].mean()
        
    var_mean_range = [chosen_var_mean_value - (chosen_var_mean_value * 0.1), chosen_var_mean_value + (chosen_var_mean_value * 0.1)]
    
    filtered_df = df[(df[genre_col] == chosen_genre) & \
                     (df[chosen_var] >= var_mean_range[0]) & \
                     (df[chosen_var] <= var_mean_range[1])]
    
    return filtered_df  

def get_recommendations(df, genre, chosen_vars, genre_col):
    '''
    Gets top recommended track based on make_recommendation function defined above using the given user selected genre type (genre or subgenre),
    top 3 user selected variables, and user selected genre.

    Parameters
    ----------
    df : pandas.DataFrame
      Cleaned dataset generated from clean data module (whenever that is implemented).
    genre : str
      User selected genre generated from streamlit input.
    chosen_vars : list of str
      List of 3 user selected variables from streamlit input.
    genre_col : str
      String of selected genre type, resulting in playlist_genre or playlist_subgenre

    Returns
    -------
    recs_df : pandas.DataFrame
      Dataframe consisting of recommended tracks generated based on all parameters with all duplicate tracks dropped.

    Notes
    -----
     - Loudness variable was removed for the time being until further discussion on it's necessity. We can always use the abs. value instead.
     - Example usage is implemented to see what variable types we will need to make our variables in order for the code to function properly. 
     - Currently only utilizing the first generated recommendation, but is there some other factor we want to use to choose between the final list of 5 or less tracks?
       I tried working with just setting the len requirement to 1, but it doesn't work very well. So eliminating from that final list would be better, or just generate 3 tracks?
    '''
    grouped_values = df.groupby(genre_col)
    
    all_vars = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_sec']
    all_vars = [var for var in all_vars if var not in chosen_vars] #removes already chosen variables to prevent duplicates   

    #initial recommendation based on first chosen variable (aka most preferred variable by user)
    recs_df = make_recommendation(df, grouped_values, genre, chosen_vars[0], genre_col)
    
    while len(recs_df) > 5:
        
        #iterate through chosen variables first to try and narrow down recommendations only on user preferences
        for var in chosen_vars[1:]:
            recs_df = make_recommendation(recs_df, grouped_values, genre, var, genre_col)
            if len(recs_df) <= 5:
                break
            
        for var in all_vars:
            recs_df = make_recommendation(recs_df, grouped_values, genre, var, genre_col)
            if len(recs_df) <= 5:
                break
            
    #Drops any duplicate track names/artists that may arise, maybe handle this in the cleaning module?
    recs_df = recs_df.drop_duplicates(subset=['track_name', 'track_artist'])
    return recs_df.head(1)

#Example usage
#For the recommended_tracks, we would replace the manual inputs with the user inputs returned from the streamlit web app
recommended_tracks = get_recommendations(df, 'hard rock', ['danceability', 'valence', 'energy'], 'playlist_subgenre')
print(recommended_tracks[['track_name', 'track_artist', 'danceability', 'valence', 'energy', 'track_popularity']])
