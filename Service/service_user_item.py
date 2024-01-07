import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


dataframe = pd.read_parquet('./Data/Data_ML2.parquet')  
# Calculate cosine similarity once for all data
features = dataframe[['Action', 'Casual', 'Indie', 'Simulation', 'Strategy', 'Free to Play', 'RPG', 'Sports', 'Adventure', 'Racing', 'Early Access', 'Massively Multiplayer', 'Animation &amp; Modeling', 'Video Production', 'Web Publishing', 'Education', 'Software Training', 'Utilities', 'Design &amp; Illustration', 'Audio Production', 'Photo Editing', 'Accounting']]

cosine_sim = cosine_similarity(features, features)


def recommend_user_game(user_id, num_recommendations=5):
    
    user_id = user_id.lower()
    features = dataframe[['Action', 'Casual', 'Indie', 'Simulation', 'Strategy', 'Free to Play', 'RPG', 'Sports', 'Adventure', 'Racing', 'Early Access', 'Massively Multiplayer', 'Animation &amp; Modeling', 'Video Production', 'Web Publishing', 'Education', 'Software Training', 'Utilities', 'Design &amp; Illustration', 'Audio Production', 'Photo Editing', 'Accounting']]


    cosine_sim = cosine_similarity(features, features)
    
    # Get the index of the entered user
    idx = dataframe.index[dataframe['user_id'].str.lower() == user_id].tolist()
    
    if not idx:
        return "User not found"
    
    idx = idx[0]
    
    # Get similarity scores of the entered user with other users
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort users based on similarity
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get indices of recommended games
    top_indices = [x[0] for x in sim_scores]
    
    # Get names of recommended games along with their item_id
    recommended_games = dataframe.iloc[top_indices][['id', 'title']].drop_duplicates(subset=['title']).head(num_recommendations)
    recommended_games_list = recommended_games.to_dict(orient='records')
    
    return recommended_games_list

