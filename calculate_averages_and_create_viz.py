import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def find_selected_averages(genre, var1, var2, var3, df):
    #drop unessecary columns for value graphs
    #df is cleaned df
    all_values = df.drop(columns=['track_name', 'track_artist', 'track_popularity', 'track_album_name', 'playlist_name', 'release_year', 'playlist_subgenre'])
    
    #group by genre and show bar graph and means for first selected variable of interest
    var1_values = all_values.groupby('playlist_genre')[var1].mean()
    var2_values = all_values.groupby('playlist_genre')[var2].mean()
    var3_values = all_values.groupby('playlist_genre')[var3].mean()
    
    #Produce visuals for all chosen variables
    generate_visuals(genre, var1, var1_values)
    generate_visuals(genre, var2, var2_values)
    generate_visuals(genre, var3, var3_values)
    
def generate_visuals(genre, var, values):
    #First creates list of genres represented in the values groups. 
    #Then assigns the color blue to all genre columns.
    #Finally, sets chosen genre column to the color red for visibility.
    genre_index = values.index.to_list()
    colors = ["b"] * len(genre_index)
    colors[genre_index.index(genre)] = "r"
    
    #Finds the max and min of the y values to better scale the bar graph.
    min_y = min(values.values)
    max_y = max(values.values)
    
    #Creates the bar graph plot.
    #Adds a horizontal line at the mean of the chosen genre for easier comparisons
    fig, ax = plt.subplots()
    plt.ylim([min_y-0.5*(max_y-min_y), max_y+0.25*(max_y-min_y)])
    plt.axhline(y=values[genre], color='black', linestyle='--', label='Genre Mean')
    ax.bar(genre_index, values.values, color=colors)
    plt.show()
  

#Test cases
user_genre = input('Please enter in your preferred genre: ')
user_var1 = input('Please enter in your most preferred variable within music: ')
user_var2 = input('Please enter in your second preferred variable within music: ')
user_var3 = input('Please enter in your third preferred variable within music: ')


print(find_selected_averages(user_genre, user_var1, user_var2, user_var3))
