from __future__ import annotations
from constants import PlayerPosition, PlayerStats
from data_structures.hash_table import LinearProbeTable

class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N) where N is the number of PlayerStats
            Worst Case Complexity: O(N)

        """
        self.name: str = name
        self.position: PlayerPosition = position
        self.age: int = age

        # Initialise statistics
        self.statistics: LinearProbeTable[str, int] = LinearProbeTable()
        for stat in PlayerStats:
            self.statistics[stat.value] = 0

    def reset_stats(self) -> None:
        """
        Reset the stats of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N), where N is the number of PlayerStats.
            Worst Case Complexity: O(N)

        """
        for stat in PlayerStats:
            self.statistics[stat.value] = 0

    def get_name(self) -> str:
        """
        Get the name of the player

        Returns:
            str: The name of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.name

    def get_position(self) -> PlayerPosition:
        """
        Get the position of the player

        Returns:
            PlayerPosition: The position of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.position

    def get_statistics(self):
        """
        Get the statistics of the player

        Returns:
            statistics: The players' statistics

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def __setitem__(self, statistic: PlayerStats, value: int) -> None:
        """
        Set the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat
            value (int): The value of the stat

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.statistics[statistic.value] = value

    def __getitem__(self, statistic: PlayerStats) -> int:
        """
        Get the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics[statistic.value]

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity:
            Analysis not required.
        """
        return f"Player(name={self.name}, position={self.position}, age={self.age}, stats={self.statistics})"

    def __repr__(self) -> str:
        """Returns a string representation of the Player object.
        Useful for debugging or when the Player is held in another data structure."""
        return str(self)
