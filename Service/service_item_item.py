import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fastapi import HTTPException

# Load the DataFrame
df2 = pd.read_parquet('./Data/Data_ML.parquet')

# Fill missing values in the 'review' column
df2 = df2.fillna("")

# Initialize the TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Apply TF-IDF to the 'review' column
tfidf_matrix = tfidf.fit_transform(df2['review'])

# Calculate cosine similarity using linear_kernel
cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

def recommend_game(game_id: int):
    try:
        # Check if the game ID exists in the DataFrame
        if game_id not in df2['id'].index:
            raise HTTPException(status_code=404, detail='Game ID not found.')

        # Get the title for the given game ID
        title = df2.loc[df2['id'] == game_id, 'title'].iloc[0]

        # Get the index of the game in the DataFrame
        idx = df2[df2['title'] == title].index[0]

        # Calculate cosine similarity for the specific game
        sim_cosine = list(enumerate(cosine_similarity[idx]))

        # Sort the games based on similarity scores
        sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)

        # Get the indices of the recommended games (excluding the original game)
        sim_indices = [i for i, _ in sim_scores[1:6]]

        # Get the titles of the recommended games
        sim_games = df2['title'].iloc[sim_indices].values.tolist()

        return {'original_game': {'id': game_id, 'title': title},
                'recommended_games': list(sim_games)}

    except Exception as e:
       return {'error': f'An error occurred: {str(e)}'}
    

    
