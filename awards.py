from __future__ import annotations
from data_structures.referential_array import ArrayR
from constants import PlayerStats
from season import Season


class Awards:
    def __init__(self, season: Season, player_stat: PlayerStats, num_top_players: int) -> None:
        """
        Initializes the awards based on the provided teams, player stat and top players.

        Args:
            season (season): The season we are generating the awards for.
            player_stat (PlayerStat): The player stat to order the awards by (in descending order)
            num_top_players (int): The number of players from each team to track.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.season = season
        self.player_stat = player_stat
        self.num_top_players = num_top_players

    def get_leaderboard(self) -> ArrayR[ArrayR[int | str]]:
        """
        Generates the leaderboard of awards.

        Returns:
            ArrayR(ArrayR[ArrayR[int | str]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Player Name (str)
                    - Games Played (int)
                    - Goals (int)
                    - Assists (int)
                    - Tackles (int)
                    - Interceptions (int)
                    - Star Skill (int)
                    - Weak Foot Ability (int)
                    - Weight (int)
                    - Height (int)

        Complexity:
            Best Case Complexity: O(T * P^2), where T is the number of teams, P is the number of players per team.
            Worst Case Complexity: O(T * P^2)
        """
        leaderboard = []

        teams = self.season.get_teams()
        for team in teams:
            top_players = team.get_top_x_players(self.player_stat, self.num_top_players)
            for stat_value, player_name, player in top_players:
                player_stats_array = ArrayR(10)
                player_stats_array[0] = player.get_name()
                player_stats_array[1] = player[PlayerStats.GAMES_PLAYED]
                player_stats_array[2] = player[PlayerStats.GOALS]
                player_stats_array[3] = player[PlayerStats.ASSISTS]
                player_stats_array[4] = player[PlayerStats.TACKLES]
                player_stats_array[5] = player[PlayerStats.INTERCEPTIONS]
                player_stats_array[6] = player[PlayerStats.STAR_SKILL]
                player_stats_array[7] = player[PlayerStats.WEAK_FOOT_ABILITY]
                player_stats_array[8] = player[PlayerStats.WEIGHT]
                player_stats_array[9] = player[PlayerStats.HEIGHT]
                leaderboard.append(player_stats_array)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the awards object.

        Complexity:
            Analysis not required.
        """
        return f"Awards for stat {self.player_stat.value} with top {self.num_top_players} players per team."

    def __repr__(self) -> str:
        """Returns a string representation of the Awards object.
        Useful for debugging or when the Awards are held in another data structure."""
        return str(self)
