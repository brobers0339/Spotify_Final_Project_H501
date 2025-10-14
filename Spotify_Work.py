import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Cleaned dataset
url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
df = pd.read_csv(url)

df["track_album_release_date"] = pd.to_datetime(df["track_album_release_date"], errors="coerce")
df["release_year"] = df["track_album_release_date"].dt.year.astype("Int64")

df = df.drop(columns=["track_id","track_album_id","playlist_id","track_album_release_date"])
df = df[df["release_year"]>=2015]
df = df.fillna("Unknown")

def find_selected_averages(genre, var1, var2, var3):
  '''
  This function groups the dataset by playlist genres and the selected vars (1, 2, and 3). 
  Then it calls the generate_visual function to generate visuals to display the averages of each
  playlist genre under the selected variable.
  '''
    #drop unessecary columns for value graphs
    all_values = df.drop(columns=['track_name', 'track_artist', 'track_popularity', 'track_album_name', 'playlist_name', 'release_year', 'playlist_subgenre'])
    
    #group by genre and show bar graph and means for first selected variable of interest
    var1_values = all_values.groupby('playlist_genre')[var1].mean()
    var2_values = all_values.groupby('playlist_genre')[var2].mean()
    var3_values = all_values.groupby('playlist_genre')[var3].mean()
    
    generate_visual(genre, var1, var1_values)
    generate_visual(genre, var2, var2_values)
    generate_visual(genre, var3, var3_values)
    
def generate_visual(genre, var, values):
  '''
  This function wll generate the visuals to display the average values for each of the selected variables
  and highlights the selected genres by making the column red.
  '''
    genre_index = values.index.to_list()
    colors = ["b"] * len(genre_index)
    colors[genre_index.index(genre)] = "r"
    
    fig, ax = plt.subplots()
    ax.bar(genre_index, values.values, color=colors)
    plt.show()
  

#Test cases
user_genre = input('Please enter in your preferred genre: ')
user_var1 = input('Please enter in your most preferred variable within music: ')
user_var2 = input('Please enter in your second preferred variable within music: ')
user_var3 = input('Please enter in your third preferred variable within music: ')


print(find_selected_averages(user_genre, user_var1, user_var2, user_var3))
