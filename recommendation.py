import pandas as pd
#merging logic from original recommendation code
def make_recommendation(df: pd.DataFrame, grouped_df, chosen_genre: str, chosen_var: str, genre_col: str) -> pd.DataFrame:
    """
    > Filter df for chosen_genre and chosen_var within +/- 50% of the group's mean.
      SORT the results by how close they are to the mean, so the best matches come first.
    """
    if chosen_var not in df.columns:
        return pd.DataFrame()  # nothing to do

    # if the group doesn't exist, return empty
#-----RECOMMENDATION MODULE-----#
#recommendation.py
#-----IMPORTS-----#
import pandas as pd
#-------------------------------------------------------------------#
#-----RECOMMENDATION LOGIC-----#
#merging logic from original recommendation code
def make_recommendation(df: pd.DataFrame, grouped_df, chosen_genre: str, chosen_var: str, genre_col: str) -> pd.DataFrame:
    """
    > Filter df for chosen_genre and chosen_var within +/-10% of the group's mean.

    """
    if chosen_var not in df.columns:
        return pd.DataFrame()  #nothing to do

    #if the group doesn't exist, return empty
    try:
        group = grouped_df.get_group(chosen_genre)
    except Exception:
        return pd.DataFrame()

    chosen_var_mean_value = group[chosen_var].mean()
    if pd.isna(chosen_var_mean_value):
        return pd.DataFrame()

    # Your loosened 50% range
    var_mean_range = [chosen_var_mean_value - (chosen_var_mean_value * 0.5),
                      chosen_var_mean_value + (chosen_var_mean_value * 0.5)]

    # Filter
    filtered_df = df[(df[genre_col] == chosen_genre) &
                     (df[chosen_var] >= var_mean_range[0]) &
                     (df[chosen_var] <= var_mean_range[1])].copy() # .copy() ensures we can modify it below

    # --- THE FIX: SORT BY CLOSENESS TO MEAN ---
    # We calculate the absolute difference between the song's value and the group mean
    # Songs with a smaller difference (closer to the mean) will appear at the top
    filtered_df['similarity_score'] = (filtered_df[chosen_var] - chosen_var_mean_value).abs()
    filtered_df = filtered_df.sort_values('similarity_score', ascending=True)
    
    # Clean up the helper column so it doesn't mess up future logic
    filtered_df = filtered_df.drop(columns=['similarity_score'])

    return filtered_df

    var_mean_range = [chosen_var_mean_value - (chosen_var_mean_value * 0.1),
                      chosen_var_mean_value + (chosen_var_mean_value * 0.1)]

    filtered_df = df[(df[genre_col] == chosen_genre) &
                     (df[chosen_var] >= var_mean_range[0]) &
                     (df[chosen_var] <= var_mean_range[1])]

    return filtered_df


def get_recommendations(df: pd.DataFrame, genre: str, chosen_vars: list, genre_col: str) -> pd.DataFrame:
    """
    >   Return top recommended tracks for the given genre and chosen vars.
        Attempts to narrow to <= 5 tracks by iteratively applying chosen and other features.
        Returns first row (head(1)) as a single recommendation (to match previous behavior).

    """
    if genre_col not in df.columns:
        return pd.DataFrame()

    grouped_values = df.groupby(genre_col)

    all_vars = ['danceability', 'energy', 'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_sec']
    all_vars = [var for var in all_vars if var not in chosen_vars and var in df.columns]

    #initial recommendation based on first chosen variable
    recs_df = make_recommendation(df, grouped_values, genre, chosen_vars[0], genre_col)
    #if no result, return empty
    if recs_df.empty:
        return pd.DataFrame()

    #try to shrink to <= 5 using chosen_vars and then other vars
    while len(recs_df) > 20:
        while len(recs_df) > 5:
            stop_while = False

            for var in chosen_vars[1:]:
                last_recs_df = recs_df
                recs_df = make_recommendation(recs_df, grouped_values, genre, var, genre_col)
                if len(recs_df) <= 20:
                    if len(recs_df) == 0:
                        recs_df = last_recs_df
                        stop_while = True
                    break

            for var in all_vars:
                last_recs_df = recs_df
                recs_df = make_recommendation(recs_df, grouped_values, genre, var, genre_col)
                if len(recs_df) <= 20:
                    if len(recs_df) == 0:
                        recs_df = last_recs_df
                        stop_while = True
                    break

            if stop_while:
                break

            #if we loop forever (defensive), break
            if len(recs_df) == 0:
                break

    #drops duplicates on track + artist then return the first recommendation
    if not recs_df.empty and {'track_name', 'track_artist'}.issubset(recs_df.columns):
        recs_df = recs_df.drop_duplicates(subset = ['track_name', 'track_artist'])

    return recs_df.head(4)  # Return up to 4 recommendations
