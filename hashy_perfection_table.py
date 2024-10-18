""" Hash Table ADT using a Perfect Hash Table """
from __future__ import annotations
__author__ = 'Brendon Taylor'
__since__ = '22/08/2024'

from data_structures.referential_array import ArrayR
from typing import Generic, Union, TypeVar
from constants import PlayerStats

K = TypeVar('K')
V = TypeVar('V')


class HashyPerfectionTable(Generic[K, V]):
    """
    HashyPerfectionTable holds a perfect hash function for a small set of known keys.
    The expected keys can be found within constants.py in the PlayerStats enum.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    def __init__(self) -> None:
        """
        Initialise the Hash Table.
        Note: Our default table size 13, if you increase it to 19, you will not get full marks for approach.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.array: ArrayR[Union[tuple[K, V], None]] = ArrayR(13)
        self.count: int = 0

    # Create a mapping from key to index, with a class variable
    _key_to_index = {stat.value: idx for idx, stat in enumerate(PlayerStats)}

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        try:
            return self._key_to_index[key]
        except KeyError:
            raise KeyError(f"Invalid key: {key}")

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def keys(self) -> ArrayR[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(M), where M is the size of the array.
        """
        res = ArrayR(len(self.array))
        i = 0
        for x in range(len(self)):
            if self.array[x] is not None:
                res[i] = self.array[x][0]
                i += 1
        return res

    def values(self) -> ArrayR[V]:
        """
        Returns all values in the hash table.

        :complexity: O(M), where M is the size of the array.
        """
        res = ArrayR(len(self.array))
        i = 0
        for x in range(len(self)):
            if self.array[x] is not None:
                res[i] = self.array[x][1]
                i += 1
        return res

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        Complexity:
        Best Case Complexity: O(self[key])
        Worst Case Complexity: O(self[key])
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Raises:
        KeyError: When the key doesn't exist.
        """
        position: int = self.hash(key)
        if self.array[position] is None:
            raise KeyError(f"{key} not found")
        return self.array[position][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Raises:
        KeyError: When the key doesn't exist.
        """
        position: int = self.hash(key)

        if self.array[position] is None:
            self.count += 1

        self.array[position] = (key, data)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Raises:
        KeyError: When the key doesn't exist.
        """
        position: int = self.hash(key)
        self.array[position] = None
        self.count -= 1

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == len(self.array)

    def __str__(self) -> str:
        """
        Complexity:
            Best Case Complexity: O(M), where M is the size of the array.
            Worst Case Complexity: O(M)
        """
        result: str = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
