from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from dataclasses import dataclass
from game_simulator import GameSimulator
from team import Team
from constants import GameResult, ResultStats, TeamStats, PlayerStats
from typing import Generator, Union


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team
    away_team: Team


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week
        self.current_index: int = 0

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        self.current_index = 0
        return self

    def __next__(self):
        """
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        if self.current_index < len(self.games):
            game = self.games[self.current_index]
            self.current_index += 1
            return game
        else:
            raise StopIteration


class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(T^2), where T is the number of teams.
            Worst Case Complexity: O(T^2)
        """
        self.teams = teams
        self.schedule = LinkedList()
        self.leaderboard = ArrayR(len(teams))
        for i in range(len(teams)):
            self.leaderboard[i] = teams[i]
        # Sort leaderboard by team name first
        self.leaderboard = self.__sort_leaderboard(self.leaderboard)
        # Generate schedule
        raw_schedule = self._generate_schedule()
        for i, week_games in enumerate(raw_schedule):
            week = WeekOfGames(i + 1, week_games)
            self.schedule.append(week)

    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(T^2) where T is the number of teams in the season.
            Worst Case Complexity: O(T^2)
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity: O(T^3 * P), where T is the number of teams, P is the maximum number of players per team.
            Worst Case Complexity: O(T^3 * P)
        """
        for game in self.get_next_game():
            result = GameSimulator.simulate(game.home_team, game.away_team)
            # Update team statistics
            home_goals = result[ResultStats.HOME_GOALS.value]
            away_goals = result[ResultStats.AWAY_GOALS.value]

            # Update team goals
            game.home_team[TeamStats.GOALS_FOR] += home_goals
            game.home_team[TeamStats.GOALS_AGAINST] += away_goals
            game.away_team[TeamStats.GOALS_FOR] += away_goals
            game.away_team[TeamStats.GOALS_AGAINST] += home_goals

            # Update goal difference
            game.home_team[TeamStats.GOALS_DIFFERENCE] = game.home_team[TeamStats.GOALS_FOR] - game.home_team[
                TeamStats.GOALS_AGAINST]
            game.away_team[TeamStats.GOALS_DIFFERENCE] = game.away_team[TeamStats.GOALS_FOR] - game.away_team[
                TeamStats.GOALS_AGAINST]

            # Update wins, draws, losses, points, and last five results
            if home_goals > away_goals:
                game.home_team[TeamStats.WINS] += 1
                game.away_team[TeamStats.LOSSES] += 1
            elif home_goals < away_goals:
                game.home_team[TeamStats.LOSSES] += 1
                game.away_team[TeamStats.WINS] += 1
            else:
                game.home_team[TeamStats.DRAWS] += 1
                game.away_team[TeamStats.DRAWS] += 1

            # Update player statistics
            goal_scorers = result[ResultStats.GOAL_SCORERS.value]
            goal_assists = result[ResultStats.GOAL_ASSISTS.value]
            tackles = result[ResultStats.TACKLES.value]
            interceptions = result[ResultStats.INTERCEPTIONS.value]

            if goal_scorers is not None:
                for scorer_name in goal_scorers:
                    player = self.__find_player_by_name(scorer_name)
                    if player:
                        player[PlayerStats.GOALS] += 1

            if goal_assists is not None:
                for assist_name in goal_assists:
                    player = self.__find_player_by_name(assist_name)
                    if player:
                        player[PlayerStats.ASSISTS] += 1

            if tackles is not None:
                for tackler_name in tackles:
                    player = self.__find_player_by_name(tackler_name)
                    if player:
                        player[PlayerStats.TACKLES] += 1

            if interceptions is not None:
                for interceptor_name in interceptions:
                    player = self.__find_player_by_name(interceptor_name)
                    if player:
                        player[PlayerStats.INTERCEPTIONS] += 1

            # After simulating all games, update the leaderboard
        self.leaderboard = self.__sort_leaderboard_by_stats(self.leaderboard)

    def __find_player_by_name(self, name: str) -> Union[Player, None]:
        """
        Finds a player by name among all teams.

        Complexity:
            Best Case Complexity: O(1), if the player is found in the first team.
            Worst Case Complexity: O(T * P), where T is the number of teams, P is the maximum number of players per team.
        """
        for team in self.teams:
            players = team.get_players()
            if players is None:
                continue
            for player in players:
                if player.get_name() == name:
                    return player
        return None

    def __sort_leaderboard(self, leaderboard: ArrayR[Team]) -> ArrayR[Team]:
        """
        Sorts the leaderboard by team name.

        Complexity:
            Best Case Complexity: O(T^2), where T is the number of teams.
            Worst Case Complexity: O(T^2)
        """
        # Simple insertion sort
        for i in range(1, len(leaderboard)):
            key = leaderboard[i]
            j = i - 1
            while j >= 0 and leaderboard[j].get_name() > key.get_name():
                leaderboard[j + 1] = leaderboard[j]
                j -= 1
            leaderboard[j + 1] = key
        return leaderboard

    def __sort_leaderboard_by_stats(self, leaderboard: ArrayR[Team]) -> ArrayR[Team]:
        """
        Sorts the leaderboard based on points, goal difference, goals for, and team name.

        Complexity:
            Best Case Complexity: O(T^2), where T is the number of teams.
            Worst Case Complexity: O(T^2)
        """
        # Insertion sort
        for i in range(1, len(leaderboard)):
            key = leaderboard[i]
            j = i - 1
            while j >= 0 and self.__compare_teams(key, leaderboard[j]):
                leaderboard[j + 1] = leaderboard[j]
                j -= 1
            leaderboard[j + 1] = key
        return leaderboard

    def __compare_teams(self, team1: Team, team2: Team) -> bool:
        """
        Returns True if team1 should come before team2.

        Complexity: O(1)
        """
        if team1[TeamStats.POINTS] > team2[TeamStats.POINTS]:
            return True
        elif team1[TeamStats.POINTS] == team2[TeamStats.POINTS]:
            if team1[TeamStats.GOALS_DIFFERENCE] > team2[TeamStats.GOALS_DIFFERENCE]:
                return True
            elif team1[TeamStats.GOALS_DIFFERENCE] == team2[TeamStats.GOALS_DIFFERENCE]:
                if team1[TeamStats.GOALS_FOR] > team2[TeamStats.GOALS_FOR]:
                    return True
                elif team1[TeamStats.GOALS_FOR] == team2[TeamStats.GOALS_FOR]:
                    return team1.get_name() < team2.get_name()
        return False

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(1), if moving within the same position.
            Worst Case Complexity: O(W), where W is the number of weeks in the season.
        """
        if orig_week < 1 or orig_week > len(self.schedule):
            raise ValueError("Invalid original week")
        if new_week is not None and (new_week < 1 or new_week > len(self.schedule)):
            raise ValueError("Invalid new week")

        orig_week_index = orig_week - 1
        week_to_move = self.schedule[orig_week_index]
        self.schedule.delete_at_index(orig_week_index)

        if new_week is None:
            # Move to the end of the season
            self.schedule.append(week_to_move)
        else:
            new_week_index = new_week - 1
            self.schedule.insert(new_week_index, week_to_move)

    def get_next_game(self) -> Generator[Game, None, None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: O(1) per game retrieval.
            Worst Case Complexity: O(1) per game retrieval.
        """
        for week in self.schedule:
            for game in week:
                yield game

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity: O(T), where T is the number of teams.
            Worst Case Complexity: O(T)
        """
        leaderboard_data = ArrayR(len(self.leaderboard))
        for i, team in enumerate(self.leaderboard):
            team_data = ArrayR(10)
            team_data[0] = team.get_name()
            team_data[1] = team[TeamStats.GAMES_PLAYED]
            team_data[2] = team[TeamStats.POINTS]
            team_data[3] = team[TeamStats.WINS]
            team_data[4] = team[TeamStats.DRAWS]
            team_data[5] = team[TeamStats.LOSSES]
            team_data[6] = team[TeamStats.GOALS_FOR]
            team_data[7] = team[TeamStats.GOALS_AGAINST]
            team_data[8] = team[TeamStats.GOALS_DIFFERENCE]
            last_five = team.get_last_five_results()
            if last_five is not None:
                last_five_results = ArrayR(len(last_five))
                for j, result in enumerate(last_five):
                    last_five_results[j] = result
                team_data[9] = last_five_results
            else:
                team_data[9] = ArrayR(0)
            leaderboard_data[i] = team_data
        return leaderboard_data

    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.teams

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return f"Season with {len(self.teams)} teams."

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
