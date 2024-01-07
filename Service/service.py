import pandas as pd

GENRE_COLUMN = 'genre'
PLAYTIME_COLUMN = 'playtime_forever'
YEAR_COLUMN = 'year'
RECOMMEND_COLUMN = 'recommend'
TITLE_COLUMN = 'title'
DEVELOPER_COLUMN = 'developer'
SENTIMENT_COLUMN = 'sentiment_analysis'
USER_COLUMN = 'user_id'

def generate_api_homepage():
    html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steam API</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #34495e; /* Lighter background color */
            color: #ecf0f1;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        header {
            background-color: #2c3e50; /* Dark gray color */
            color: #fff;
            padding: 15px;
            text-align: center;
            width: 100%;
        }
        h1 {
            margin-top: 20px;
            color: #ecf0f1;
        }
        p {
            color: #bdc3c7;
            text-align: center;
            font-size: 16px;
            margin-top: 10px; /* Optional: Adjust the top margin */
            line-height: 1.5;
        }
        span {
            background-color: #e74c3c;
            padding: 5px;
            border-radius: 5px;
            color: #fff;
        }
        a {
            text-decoration: none;
            color: #3498db;
            font-weight: bold;
        }
        img {
            vertical-align: middle;
            margin-top: 10px;
            max-width: 100%;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        footer {
            margin-top: auto;
            padding: 20px;
            color: #fff;
            text-align: center;
            background-color: #2c3e50; /* Dark gray color */
            color: #fff;
            width: 100%;
        }
    </style>
</head>
<body>
    <header>
        <h1>Steam Games API</h1>
    </header>
    <p>Welcome to the Steam Games API, where you can make various queries about the gaming platform.</p>
    <p>INSTRUCTIONS:</p>
    <p>Type <span>/docs</span> after the current URL to interact with the API. Or <a href="http://127.0.0.1:8000/docs">click here</a> to view the API documentation.</p>
    <p>Visit my profile on <a href="https://www.linkedin.com/in/mateo-lopez-ba06861b3/" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin"></a></p>
    <p>Project development is on <a href="https://github.com/luifa04/Project1_MLOps" target="_blank"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
    <footer>
        © 2024 Steam Games API. All rights reserved.
    </footer>
</body>
</html>
    '''
    return html_code


def get_max_playtime_year(df, genre: str) -> int:
    """
    Get the year with the maximum total playtime for the specified genre.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the game data.
    - genre (str): The genre to filter.

    Returns:
    - int: The year with the most playtime.
    """
    try:
        genre_df = df[df[genre] == 1]

        if genre_df.empty:
            raise KeyError(f"No data found for the genre: {genre}")

        year_playtime_df = genre_df.groupby(YEAR_COLUMN)[PLAYTIME_COLUMN].sum().reset_index()
        max_playtime_year = year_playtime_df.loc[year_playtime_df[PLAYTIME_COLUMN].idxmax(), YEAR_COLUMN]

        return int(max_playtime_year)
    except KeyError as e:
        return -1  
    


def get_user_with_max_playtime(df, genre: str):
    """
    Get the user with the maximum total playtime for the specified genre,
    along with a list of accumulated playtime by year.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the game data.
    - genre (str): The genre to filter.

    Returns:
    - dict: {"Usuario con más horas jugadas para Género X": user_id, "Horas jugadas": [{"Año": year, "Horas": total_playtime}, ...]}
    """
    try: 
        genre = genre.capitalize()
        if genre not in df.columns:
            return {"Error": f"Genre {genre} not found in the dataset."}

        genre_df = df[df[genre] == 1]

        if genre_df.empty:
            return {"Error": f"No data found for the genre: {genre}"}

        user_with_max_playtime = genre_df.groupby(USER_COLUMN)[PLAYTIME_COLUMN].sum().idxmax()
        user_df = genre_df[genre_df[USER_COLUMN] == user_with_max_playtime]
        playtime_by_year = user_df.groupby(YEAR_COLUMN)[PLAYTIME_COLUMN].sum().reset_index()

        result = {
            "Usuario con más horas jugadas para Género {}".format(genre): user_with_max_playtime,
            "Horas jugadas": playtime_by_year.to_dict(orient='records'),
        }

        return result
    except KeyError as e:
        return {"Error": str(e)}






def get_top_recommended_games(df, year: int):
    """
    Get the top 3 games most recommended by users for the specified year.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the game data.
    - year (int): The year to filter.

    Returns:
    - list: [{"Rank 1": game_title}, {"Rank 2": game_title}, {"Rank 3": game_title}]
    """
    try:
        year_df = df[df[YEAR_COLUMN] == year]

        if year_df.empty:
            raise KeyError(f"No data found for the year: {year}")

        recommended_games = year_df[(year_df[RECOMMEND_COLUMN] == True) & (year_df[SENTIMENT_COLUMN] >= 1)][TITLE_COLUMN]
        top_recommended_games = recommended_games.value_counts().nlargest(3).index

        result = [{"Rank {}".format(i + 1): game_title} for i, game_title in enumerate(top_recommended_games)]

        return result
    except KeyError as e:
        return -1
    

def get_worst_developers(df, year: str):
    """
    Get the top 3 developers with the least recommended games by users for the specified year.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the game data.
    - year (str): The year to filter.

    Returns:
    - list: [{"Rank 1": developer_name}, {"Rank 2": developer_name}, {"Rank 3": developer_name}]
    """
    try:
        year_df = df[df['posted year'] == year]

        if year_df.empty:
            raise KeyError(f"No data found for the year: {year}")

        # Filter games with negative sentiment and not recommended
        worst_developers = year_df[(year_df[SENTIMENT_COLUMN] == 0) & (year_df[RECOMMEND_COLUMN] == False)][DEVELOPER_COLUMN]
        top_worst_developers = worst_developers.value_counts().nlargest(3).index

        result = [{"Rank {}".format(i + 1): developer_name} for i, developer_name in enumerate(top_worst_developers)]

        return result
    except KeyError as e:
        return -1

def sentiment_analysis(df, developer: str):
    """
    Get sentiment analysis for reviews based on the developer.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the game data.
    - developer (str): The developer to filter.

    Returns:
    - dict: {developer_name: {'Negative': Negative_count, 'Neutral': Neutral_count, 'Positive': Positive_count}}
    """
    try:
        # Filter the DataFrame for the specific developer
        developer_df = df[df[DEVELOPER_COLUMN] == developer]

        # Check if there is no data for the developer
        if developer_df.empty:
            raise KeyError(f"No data found for the developer: {developer}")

        # Map sentiment values to labels
        sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}

        # Count the frequencies of each value in the 'sentiment' column for the specific developer
        sentiment_counts = developer_df[SENTIMENT_COLUMN].map(sentiment_mapping).value_counts().to_dict()

        result = {developer: {sentiment_label: sentiment_counts.get(sentiment_label, 0) for sentiment_label in ['Negative', 'Neutral', 'Positive']}}
        return result
    except KeyError as e:
        return -1


