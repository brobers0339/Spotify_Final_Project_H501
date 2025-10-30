def make_recommendation():
  '''
  This code is a very rough outline of what I'd like to have the final product look like (major brain dump on my end of just doing trial and error with a bit of copilot input).
  
  My idea is to have the filtered data (all_values in this case) be the top tier of data that we will pull from and then we will continue to filter down based on the calculated ranges
  for the mean of that given variable. 

  What I Have Working
  -------------------
  I have the all_values working and properly grouped. Only issue is my code is only currently utilizing the genre tab, but I don't see the implementation of subgenres being much of an issue.
  I am able to retrieve the mean value of the given genre and variable from the all_values.
  I am able to calculate the mean range that will be used to find the recommended songs.

  Current Issues
  --------------
  I really just haven't had enough time to really sit down and work on this. I have an idea of what is going wrong and just need to mess with it some more!
  '''
  
    #First get rid of unecessary columns from the data frame so we just have the genre, subgenre, and all corresponding and affected variables we are studying.
    all_values = df.drop(columns=['track_name', 'track_artist', 'track_album_name', 'playlist_name', 'release_year', 'playlist_subgenre'])
  
    #Group by playlist genre, will need to make this a dynamic variable depending on what the user chooses (sub genre or genre). 
    all_values = all_values.groupby('playlist_genre')

    #Example case to start, but will be modifying this to use inputted variables instead.
    chosen_var_mean_value = all_values.get_group('rap')['tempo'].mean()

    #Very basic mean range to use while I am still testing out my code.
    #Not sure if we should make this dynamic or moreso how we should make this dynamic, 
    #but the range will definitely need to be adjuted when accounting for the much larger values.
    var_mean_range = [chosen_var_mean_value - .5, chosen_var_mean_value + .5]

    #This line doesn't work right now!
    #Idea for this is to access the original filetered dataset and only retrieve the instances of the given genre that have the   
    #tempo within the calculated range above.
    #filtered_df = all_values[(all_values.get_group('rap')['tempo'] >= var_mean_range[0]) & (all_values.get_group('rap')['tempo'] <= var_mean_range[1])]

