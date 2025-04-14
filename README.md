Project: NBA Team Insights with FastAPI & Ball Don’t Lie API
Tech Stack: Python, FastAPI, Ball Don’t Lie API, Uvicorn
Project Overview:
This web service, built using FastAPI, provides detailed insights into NBA teams by integrating with the Ball Don’t Lie API. The project includes endpoints that let users:
•	Fetch basic team information (name, city, abbreviation)
•	Retrieve all games played by a team in the 2023–2024 season
•	Compute the average home game score for a team within a custom date range
Endpoints & Data Flow:
/team/{team_id}
Fetches metadata (team name, city, abbreviation) for a given team ID by calling the Ball Don’t Lie teams endpoint.
/games/last?team_id={id}
Returns a JSON object with all the games played by the team in the 2023–2024 season.
•	Behind the scenes: The endpoint makes a GET request to the API with specific date filters (2023-10-18 to 2024-04-09) and the team ID.
/games/avg?team_id={id}&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
Calculates the average home team score for games played during the user-defined date range.
•	Logic:
1.	Fetch all games in the date range.
2.	Extract the home_team_score for each.
3.	Compute the average using Python list comprehension and basic math.
•	Data Flow Diagram (Summary):
•	User → FastAPI Endpoint → Ball Don’t Lie API → JSON Response → Data Parsing → Response Output
Libraries & Functions Used:
•	requests: For API calls
•	uvicorn: To run the server
•	Custom functions like check_team(), get_team_games(), and avg_home_scores() abstract the data fetching and transformation logic
