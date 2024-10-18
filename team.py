from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.hash_table import LinearProbeTable
from data_structures.linked_list import LinkedList
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar

T = TypeVar("T")


class Team:
    _team_counter = 0

    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity: O(P), where P is the number of players in the team.
            Worst Case Complexity: O(P)
        """
        self.number = Team._team_counter
        Team._team_counter += 1

        self.name = team_name
        self.statistics = LinearProbeTable()
        for stat in TeamStats:
            if stat == TeamStats.LAST_FIVE_RESULTS:
                self.statistics[stat.value] = LinkedList()
            else:
                self.statistics[stat.value] = 0

        self.players = LinearProbeTable()
        for player in players:
            self.add_player(player)

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        for stat in TeamStats:
            if stat == TeamStats.LAST_FIVE_RESULTS:
                self.statistics[stat.value] = LinkedList()
            else:
                self.statistics[stat.value] = 0

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        position = player.get_position().value  # Convert enum to string
        if position not in self.players:
            self.players[position] = LinkedList()
        self.players[position].append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1), if the player is at the beginning of the list.
            Worst Case Complexity: O(N_p^2), where N_p is the number of players in that position.

        """
        position = player.get_position().value  # Convert enum to string
        if position in self.players:
            player_list = self.players[position]
            index = 0
            while index < len(player_list):
                if player_list[index] == player:
                    player_list.delete_at_index(index)
                    break
                index += 1
            if len(player_list) == 0:
                del self.players[position]

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity: O(1), when position is specified.
            Worst Case Complexity: O(N), where N is the total number of players in the team, when position is None.

        """
        if position is None:
            players_list = []
            for pos in PlayerPosition:
                pos_value = pos.value
                if pos_value in self.players:
                    for player in self.players[pos_value]:
                        players_list.append(player)
            if not players_list:
                return None
            return ArrayR.from_list(players_list)
        else:
            position_value = position.value
            if position_value in self.players:
                return self.players[position_value]
            else:
                return None

    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        last_five = self.statistics[TeamStats.LAST_FIVE_RESULTS.value]
        if len(last_five) == 0:
            return None
        else:
            return last_five

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity: O(N), where N is the number of players in the team.
            Worst Case Complexity: O(N)
        """
        old_value = self.statistics[statistic.value]
        self.statistics[statistic.value] = value

        if statistic == TeamStats.WINS:
            delta = value - old_value
            self.statistics[TeamStats.POINTS.value] += delta * GameResult.WIN.value
            self.statistics[TeamStats.GAMES_PLAYED.value] += delta
            self.__update_last_five_results(GameResult.WIN, delta)
            self.__update_players_games_played(delta)
        elif statistic == TeamStats.DRAWS:
            delta = value - old_value
            self.statistics[TeamStats.POINTS.value] += delta * GameResult.DRAW.value
            self.statistics[TeamStats.GAMES_PLAYED.value] += delta
            self.__update_last_five_results(GameResult.DRAW, delta)
            self.__update_players_games_played(delta)
        elif statistic == TeamStats.LOSSES:
            delta = value - old_value
            self.statistics[TeamStats.GAMES_PLAYED.value] += delta
            self.__update_last_five_results(GameResult.LOSS, delta)
            self.__update_players_games_played(delta)
        elif statistic == TeamStats.GOALS_FOR:
            delta = value - old_value
            self.statistics[TeamStats.GOALS_DIFFERENCE.value] += delta
        elif statistic == TeamStats.GOALS_AGAINST:
            delta = value - old_value
            self.statistics[TeamStats.GOALS_DIFFERENCE.value] -= delta
        else:
            self.statistics[statistic.value] = value

    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics[statistic.value]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(1), if team has no players.
            Worst Case Complexity: O(N), where N is the number of players in the team.
        """
        count = 0
        if not self.players.is_empty():
            for position in self.players.keys():
                count += len(self.players[position])
        return count

    def __update_last_five_results(self, result: GameResult, delta: int) -> None:
        last_five = self.statistics[TeamStats.LAST_FIVE_RESULTS.value]
        if delta > 0:
            for _ in range(delta):
                last_five.append(result)
                if len(last_five) > 5:
                    last_five.delete_at_index(0)
        elif delta < 0:
            for _ in range(-delta):
                # Remove from end
                for i in range(len(last_five) - 1, -1, -1):
                    if last_five[i] == result:
                        last_five.delete_at_index(i)
                        break

    def __update_players_games_played(self, delta: int) -> None:
        for player in self.get_players():
            player[PlayerStats.GAMES_PLAYED] += delta

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return f"Team(name={self.name}, number={self.number})"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)
