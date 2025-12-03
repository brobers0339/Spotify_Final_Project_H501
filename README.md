# Spotify_Final_Project_H501

<h3><u>To run this program, do the following:</u></h3>

1. Open your terminal in the folder where these project files are stored
2. Ensure that your Python install is up to date
3. Ensure that your conda environment is active
4. Type "streamlit run main.py"
5. A new window should open up in your default browser and the webpage should appear
6. To close the application, pull up your terminal again, and hit CTRL+C to terminate the program

<h3><u>Rough draft of environment.yml:</u></h3>

```python
app:
  name: "Spotify Final Project"
  author: "..."
  debug: false
  theme:
    primary_color: "#4A90E2"
    background_color: "#F5F7FA"
    text_color: "#333333"

data:
  dataset_path: "data/songs.csv" #temp, change this to be the url or delete it from here
  id_column: "track_id"
  title_column: "track_name"
  artist_column: "artist_name"

features:
  primary_feature: "danceability"
  secondary_filters:
    - "energy"
    - "valence"
  allowed_features:
    - danceability
    - energy
    - valence
    - acousticness
    - instrumentalness
    - liveness
    - loudness
    - speechiness
    - tempo
    - duration_ms
    - key
    - mode

model:
  similarity_metric: "euclidean"   #options: euclidean, cosine
  num_recommendations: 10
  normalize_features: true

ui:
  table_page_size: 10
  show_raw_data: false
  allow_feature_override: true
  show_feature_distribution_plots: true
  show_similarity_scores: true

logging:
  level: "INFO"
  log_to_file: true
  file_path: "logs/app.log"

performance:
  cache_results: true
  cache_ttl_seconds: 600 #cache similarity computations for 10 minutes

```
