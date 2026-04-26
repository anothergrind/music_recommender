flowchart TD
    A["User Profiles<br/>mode + prefs + penalties"] --> B["CLI Runner"]
    D["songs.csv<br/>song features"] --> B
    B --> E["load_songs<br/>CSV to list of song records"]
    E --> F["recommend_songs<br/>user_prefs, songs, k, mode"]

    F --> G["score_song"]
    G --> H["Base scoring<br/>genre, mood, energy, acoustic"]
    G --> I["Advanced scoring<br/>decade, popularity, mood tags,<br/>instrumentalness, speechiness, liveness"]
    H --> J["base score + reasons"]
    I --> J

    J --> K["Diversity reranking<br/>artist penalty + genre penalty"]
    K --> L["Top-K songs + explanations"]
    L --> M["Output formatter<br/>compact table + top-3 bullets"]
    M --> N["Terminal output"]

    O["Mode weights<br/>genre_first, mood_first, energy_focused"] --> G