from   fastapi import FastAPI, Path
from   fastapi.responses import HTMLResponse
import pandas as pd
from   Service.service import generate_api_homepage,get_max_playtime_year,get_user_with_max_playtime,get_top_recommended_games,get_worst_developers,sentiment_analysis
from   Service.service_user_item import recommend_user_game
from   Service.service_item_item import recommend_game
import gzip

app=FastAPI(debug=True)

with gzip.open('Data/Games_Items_final.csv.gz', 'rt', encoding='utf-8') as f:     
    df1 = pd.read_csv(f)
#df1 = pd.read_parquet('./Data/Games_Items_final.parquet')
df2 = pd.read_parquet('./Data/Games_Reviews_final.parquet')

@app.get('/', tags=['Home'], response_class=HTMLResponse)
def message():
    return generate_api_homepage()

@app.get('/playtime-genre/{genre}',
         tags=['General Inquiries'])
def PlayTimeGenre(genre: str  = Path(..., title="Specify the genre", description="Specify the genre in the path", example="Action") ):
    genre = genre.capitalize()
    max_playtime_year = get_max_playtime_year(df1, genre)

    if max_playtime_year == -1:
        return {"error": f"No information available for the genre: {genre}"}

    return {"Genre": genre, "Year with the most playtime": max_playtime_year}


@app.get('/user-for-genre/{genre}',
         tags=['General Inquiries'])
def UserForGenre(genre: str = Path(..., title="Specify the genre", description="Specify the genre in the path", example="Racing")):
    genre = genre.capitalize()
    result = get_user_with_max_playtime(df1, genre)

    if result == -1:
        return {"error": f"No information available for the genre: {genre}"}

    return result

@app.get('/users-recommend/{year}',
         tags=['General Inquiries'])
def UsersRecommend(year: int = Path(..., title="Specify the year", description="Specify the year in the path", example="2012")):
    result = get_top_recommended_games(df2, year)

    if result == -1:
        return {"error": f"No data found for the year: {year}"}

    return result

@app.get('/users-worst-developer/{year}',
         tags=['General Inquiries'])
def UsersWorstDeveloper(year: str = Path(..., title="Specify the year", description="Specify the year in the path", example="2014")):
    result = get_worst_developers(df2, year)

    if result == -1:
        return {"error": f"No data found for the year: {year}"}

    return result

@app.get('/sentiment-analysis/{developer}',
         tags=['General Inquiries'])
def SentimentAnalysis(developer: str = Path(..., title="Specify the developer", description="Specify the developer in the path", example="Facepunch Studios")):
    developer = developer.title()
    result = sentiment_analysis(df2, developer)

    if result == -1:
        return {"error": f"No data found for the developer: {developer}"}

    return result

@app.get('/recommendation_game/{game_id}',
         tags=['Recommendation'])
def recommendation_game(game_id: int = Path(..., title="Specify the Game-ID", description="Specify the Game-ID in the path", example="220")):
    return recommend_game(game_id)


@app.get("/recommendation_user_game/{user_id}",
         tags=['Recommendation'])
async def get_user_game_recommendations(user_id: str = Path(..., title="Specify the User-ID", description="Specify the User-ID in the path", example="rotflmaoman")):
    recommendations = recommend_user_game(user_id)
    return {"user_id": user_id, "recommended_games": recommendations}