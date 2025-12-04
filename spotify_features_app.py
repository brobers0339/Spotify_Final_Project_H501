import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("spotify_songs.csv")

st.title("🎵 Average Audio Features by Genre")

# Let users select features (up to 3)
numeric_features = ['energy', 'danceability', 'valence', 'tempo', 'acousticness']
selected_features = st.multiselect(
    "Please choose up to 3 features to compare:",
    numeric_features,
    default=['energy', 'danceability', 'valence'],
    max_selections=3
)

# Compute average values by genre
avg_features = df.groupby('playlist_genre')[selected_features].mean().reset_index()

# Plot chart
fig, ax = plt.subplots(figsize=(8, 5))
avg_features.plot(
    x='playlist_genre',
    kind='bar',
    ax=ax,
    color=["#63E0B0", "#FC33FF", "#33B5FF"][:len(selected_features)], 
    edgecolor='black'
)
plt.title('Average Features by Genre')
plt.ylabel('Average Value')
plt.xticks(rotation=45)
plt.legend(title='Features')
st.pyplot(fig)
