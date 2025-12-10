import pandas as pd
class Recommendation:
    # This is the "Constructor". It runs automatically when you create a new instance of the class.
    def __init__(self, df: pd.DataFrame, chosen_genre: str, chosen_vars: list, chosen_subgenre: str):
        # We store these inputs into "self" so they can be accessed by any function inside this class later.
        self.df = df
        self.chosen_genre = chosen_genre
        self.chosen_vars = chosen_vars
        self.chosen_subgenre = chosen_subgenre
        
    #merging logic from original recommendation code
    def make_recommendation(self, df, grouped_df, given_genre, chosen_var, genre_col) -> pd.DataFrame:
        """
        > Filter df for chosen_genre and chosen_var within +/- 50% of the group's mean.
        SORT the results by how close they are to the mean, so the best matches come first.
        """
        # Safety Check: If the variable (e.g., 'energy') isn't in the dataset, stop immediately.
        if chosen_var not in df.columns:
            return pd.DataFrame()  

        # if the group doesn't exist, return empty
        try:
            group = grouped_df.get_group(given_genre)
        except Exception:
            return pd.DataFrame()
        
        # 2. Calculate the "Perfect Average"
        # We find the mean value for that variable. (e.g., Average Pop Energy = 0.6)
        chosen_var_mean_value = group[chosen_var].mean()
        if pd.isna(chosen_var_mean_value):
            return pd.DataFrame()

        # Defined "Broad Net" +/-50% range
        var_mean_range = [abs(chosen_var_mean_value - (chosen_var_mean_value * 0.1)),
                        abs(chosen_var_mean_value + (chosen_var_mean_value * 0.1))]

        # Filter
        # We keep rows that match the genre AND fall inside that range.
        filtered_df = df[(df[genre_col] == given_genre) &
                        (abs(df[chosen_var]) >= var_mean_range[0]) &
                        (abs(df[chosen_var]) <= var_mean_range[1])].copy() # .copy() ensures we can modify it below

        #SORT BY CLOSENESS TO MEAN 
        # It calculates the Absolute Difference: |Song Value - Perfect Average|
        # Songs with a smaller difference (closer to the mean) will appear at the top
        filtered_df['similarity_score'] = (filtered_df[chosen_var] - chosen_var_mean_value).abs()
        filtered_df = filtered_df.sort_values('similarity_score', ascending=True)
        
        # Clean up the helper column so it doesn't mess up future logic
        filtered_df = filtered_df.drop(columns=['similarity_score'])

        return filtered_df

    def get_recommendations(self, genre_col: str) -> pd.DataFrame:
        """
        >   Return top recommended tracks for the given genre and chosen vars.
            Attempts to narrow to <= 5 tracks by iteratively applying chosen and other features.
            Returns first row (head(1)) as a single recommendation (to match previous behavior).

        """
        if genre_col not in self.df.columns:
            return pd.DataFrame()
        # We "Group" the data by genre immediately. This makes looking up averages much faster later.
        grouped_values = self.df.groupby(genre_col)

        # List of all possible variables to use for filtering
        all_vars = ['danceability', 'energy', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_sec']
        # Remove chosen_vars from all_vars to avoid repetition
        all_vars = [var for var in all_vars if var not in self.chosen_vars and var in self.df.columns]

        #initial recommendation based on first chosen variable
        if self.chosen_subgenre != "No Preferred Subgenre":
            given_genre = self.chosen_subgenre
        else:
            given_genre = self.chosen_genre
        # Make initial recommendation based on first chosen variable
        recs_df = self.make_recommendation(self.df, grouped_values, given_genre, self.chosen_vars[0], genre_col)
        #if no result, return empty
        if recs_df.empty:
            return pd.DataFrame()

        # We keep looping as long as we have more than 5 songs.
        while len(recs_df) > 5:
            stop_while = False

            # Refine using the rest of the chosen variables
            for var in self.chosen_vars[1:]:
                last_recs_df = recs_df
                # refine recommendations
                recs_df = self.make_recommendation(recs_df, grouped_values, given_genre, var, genre_col)
                
                # If we get to 5 or fewer recommendations, we can stop refining.
                if len(recs_df) <= 5:
                    if len(recs_df) == 0: #if we lost all recommendations, revert to last
                        recs_df = last_recs_df
                        stop_while = True
                    break
            
            # If we still have more than 5, start using other variables
            for var in all_vars:
                last_recs_df = recs_df
                recs_df = self.make_recommendation(recs_df, grouped_values, given_genre, var, genre_col)
                if len(recs_df) <= 5:
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
