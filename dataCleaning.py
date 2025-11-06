import pandas as pd

class SpotifyDataProcessor:
    def __init__(self, url: str):
        self.url = url
        self.df = None

    # Step 1: Load Data
    def load_data(self):
        self.df = pd.read_csv(self.url)
        return self

    # Step 2: Convert date + extract year
    def process_dates(self):
        self.df["track_album_release_date"] = pd.to_datetime(self.df["track_album_release_date"], errors="coerce")
        self.df["release_year"] = self.df["track_album_release_date"].dt.year.astype("Int64")
        return self

    # Step 3: Show songs per year
    def songs_per_year(self):
        return self.df["release_year"].value_counts().sort_index()

    # Step 4: Drop unnecessary columns
    def drop_columns(self):
        self.df = self.df.drop(columns=["track_id", "track_album_id", "playlist_id", "track_album_release_date"])
        return self

    # Step 5: Filter by year (>= 2015)
    def filter_by_year(self, year=2015):
        self.df = self.df[self.df["release_year"] >= year]
        return self

    # Step 6: Fill missing values
    def handle_missing(self):
        self.df = self.df.fillna("Unknown")
        return self

    # Step 7: Convert duration to seconds
    def convert_duration(self):
        self.df["duration_sec"] = (self.df["duration_ms"] / 1000).round(2)
        self.df = self.df.drop(columns=["duration_ms"])
        return self

    # Step 8: Get duration stats
    def duration_stats(self):
        return self.df["duration_sec"].describe()

    # Step 9: Check missing values
    def null_summary(self):
        return self.df.isnull().sum()

    # Step 10: Return final cleaned data
    def get_clean_data(self):
        return self.df


# Run directly from the same file
if __name__ == "__main__":
    URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
    
    processor = (
        SpotifyDataProcessor(URL)
        .load_data()
        .process_dates()
    )

    print("Songs Per Year:\n", processor.songs_per_year())

    processor = (
        processor
        .drop_columns()
        .filter_by_year(2015)
        .handle_missing()
        .convert_duration()
    )

    clean_df = processor.get_clean_data()

    print("\nMissing Values:\n", processor.null_summary())
    print("\nDuration Stats:\n", processor.duration_stats())
    print("\nCleaned Data (Top 5 Rows):")
    print(clean_df.head())
