from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()


def check_team(team_id):
    api_url = f"https://api.balldontlie.io/v1/teams/{team_id}"
    api_key = "0023030b-9baf-466e-8b4e-ab4098c39d7b"  # enter your api key

    headers = {"Authorization": f"{api_key}"}

    response = requests.get(api_url, headers=headers)

    # List to store the responses
    team_list = []

    if response.status_code == 200:
        team_list.append(response.json())

    # Use the key information of the list
    team_name = team_list[0]["data"]["name"]
    team_city = team_list[0]["data"]["city"]
    team_abbreviation = team_list[0]["data"]["abbreviation"]
    print(team_list)
    return team_name, team_city, team_abbreviation


def get_team_games(team_id: int, start_date: str,
                   end_date: str):  # function to get the team games
    api_url = f"https://api.balldontlie.io/v1/games?team_ids[]={team_id}&start_date={start_date}&end_date={end_date}"

    api_key = "0023030b-9baf-466e-8b4e-ab4098c39d7b"
    headers = {"Authorization": f"{api_key}"}

    response = requests.get(api_url, headers=headers)
    game_data = []
    if response.status_code == 200:
        game_data.append(response.json())

    return game_data


def avg_home_scores(team_id: int, start_date: str, end_date: str):
    api_url = f"https://api.balldontlie.io/v1/games?team_ids[]={team_id}&start_date={start_date}&end_date={end_date}"

    api_key = "0023030b-9baf-466e-8b4e-ab4098c39d7b"
    headers = {"Authorization": f"{api_key}"}

    response = requests.get(api_url, headers=headers)
    game_scores = []
    scores_for_avg = 0
    if response.status_code == 200:
        game_scores.append(response.json())

    games = game_scores[0]["data"]
    home_scores = [game["home_team_score"] for game in games]

    for i in home_scores:
        scores_for_avg += i
    avg_home_scores = round(scores_for_avg / len(home_scores), 2)
    return home_scores, avg_home_scores


#First page
@app.get("/")
def read_root():
    str_welcome = "Welcome to the BallDon API .....!"
    str_2 = f"Please enter the team id  using the end point /team/team_id."
    str_3 = f"games_info: To get games for a specific team from the last season, use the endpoint /games/last?team_id=id."
    str_4 = f"Scores info: To get Home Scores for a specific team between two given dates, use the endpoint /games/avg?team_id=id&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD.  [Note: Please Enter the dates in the format YYYY-MM-DD & DO NOT FORGET TO ENTER THE TEAM ID]"
    return {
        "Welcome Message": str_welcome,
        "team_info": str_2,
        "season_info": str_3,
        "avg_scores": str_4
    }


# Get team information
@app.get("/team/{team_id}")
def get_team_info(team_id: int, ):
    team_name, team_city, team_abbreviation = check_team(team_id)
    str_team = f"The team with id number {team_id} is {team_name}. It is located in {team_city} and the abbrevation is {team_abbreviation}"
    return {"team_info": str_team}


#get 2023-2024 season games
@app.get("/games/last")
def get_last_season_team_games(team_id: int):
    start_date = "2023-10-18"  # Start date for the 2022-2023 season
    end_date = "2024-04-09"  # End date for the 2022-2023 season

    games = get_team_games(team_id, start_date, end_date)
    return {"game_info": games}


#get avg points
@app.get("/games/avg")
def home_scores(team_id: int, start_date: str, end_date: str):
    hs, avg = avg_home_scores(team_id, start_date, end_date)
    team_name, team_city, team_abbreviation = check_team(team_id)
    games_played = len(hs)

    str_1 = f"The team {team_city} {team_name} played a total of {games_played} Home games in the given period."
    str_2 = f"The average home score for {team_city} {team_name}  was {avg} points."
    return {str_1, str_2}


uvicorn.run(app, host='0.0.0.0', port="8080")
