#-----DATA CLEANING MODULE-----#
#data_cleaning.py
#-----IMPORTS-----#
import pandas as pd
#-------------------------------------------------------------------#

def clean_spotify_df(df: pd.DataFrame, filter_year: int = 2015) -> pd.DataFrame:
    """
    >   Clean a raw spotify dataframe loaded from the raw CSV.
        Steps implemented:
            - Parse album release date -> extract release_year
            - Drop unnecessary id/album columns
            - Filter by release_year >= filter_year
            - Fill missing values
            - Convert duration_ms -> duration_sec (float)
        Returns a cleaned dataframe (copy).
    """
    df = df.copy()
    #parse dates safely
    if "track_album_release_date" in df.columns:
        df["track_album_release_date"] = pd.to_datetime(df["track_album_release_date"], errors = "coerce")
        df["release_year"] = df["track_album_release_date"].dt.year.astype("Int64")
    else:
        df["release_year"] = pd.NA

    #convert duration
    if "duration_ms" in df.columns:
        df["duration_sec"] = (df["duration_ms"] / 1000).round(2)
        #keep duration_sec and drop duration_ms
        df = df.drop(columns = ["duration_ms"], errors = "ignore")

    #drop columns that are not used for analysis to keep the dataset compact
    df = df.drop(columns = ["track_id", "track_album_id", "playlist_id", "track_album_release_date"], errors = "ignore")

    #filter by year if the column exists
    if "release_year" in df.columns:
        try:
            df = df[df["release_year"].notna() & (df["release_year"] >= filter_year)]
        except Exception:
            #if cast issuese just pass
            pass

    #replace the NaNs with "Unknown" for string fields to avoid errors when grouping
    df = df.fillna("Unknown")

    return df


#!!!Currently not called in main. Just leave for now
#utility helpers that mirror the original class
def songs_per_year(df: pd.DataFrame):
    if "release_year" in df.columns:
        return df["release_year"].value_counts().sort_index()
    return pd.Series(dtype = "int64")

def duration_stats(df: pd.DataFrame):
    if "duration_sec" in df.columns:
        return df["duration_sec"].describe()
    return pd.Series(dtype = "float")
