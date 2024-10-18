# GUIDE

# Player Stats

  1. games_played - Games played by the player this season

  2. goals - Goals scored by the player this season

  3. assists - Assists provided by the player this season

  4. tackles - Tackles made by the player this season

  5. interceptions - Interceptions made by the player this season

  6. star_skill - A star rating of the skills of the player (out of 5 stars) this season

  7. weak_foot_ability - A star rating of the weak foot ability of the player (out of 5 stars) this season

  8. weight

  9. height

# Team Stats

  1. games_played

  2. points - Points accrued by the team this season.

  3. wins - Number of wins by the team this season

  4. draws - Number of draws by the team this season

  5. losses - Number of losses by the team this season

  6. goals_for - Goals scored for the team this season

  7. goals_against - Goals scored against the team this season

  8. goals_difference - Goal difference between scored vs conceded (calculated as GOALS_FOR - GOALS_AGAINST)

  9. last_five_results - The last 5 results of the team this season

# Season Class

The Season class manages the entire football season, including the teams participating and the schedule of games.

It holds a collection of teams and provides methods to add or remove teams from the season.

The game schedule is dynamic and can change at any given game week.

The Season class includes functionality to simulate the entire season, individual games, and update team statistics based on game outcomes.

Additionally, it maintains a leaderboard to track team rankings based on their performance throughout the season.

# Award Class

The Award class, used to manage the player awards for the season, holds a:

  1. reference to the season

  2. the player stat used to allocate awards

  3. the number of players from each team that are receiving the award.

Additionally, it maintains a leaderboard to track player awards based on their performance throughout the season.

# Acknowledgements

This manager was coded as a Monash University assignment. Provided by the Monash Faculty of IT team were the scripts of generic ADT definitions, decorators, binary search, merge sort and the testcases.
