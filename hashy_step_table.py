""" Hash Table ADT

Defines a Hash Table using a modified Linear Probe implementation for conflict resolution.
"""
from __future__ import annotations
__author__ = 'Jackson Goerner'
__since__ = '07/02/2023'

from data_structures.referential_array import ArrayR
from typing import Generic, TypeVar, Union

K = TypeVar('K')
V = TypeVar('V')


class FullError(Exception):
    pass


class HashyStepTable(Generic[K, V]):
    """
    Hashy Step Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes=None) -> None:
        """
        Initialise the Hash Table.

        Complexity:
        Best Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        Worst Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array: ArrayR[Union[tuple[K, V], str, None]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        self.deleted = "<DELETED>"  # Initialise the deleted marker

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        Complexity:
        Best Case Complexity: O(len(key))
        Worst Case Complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
        """
        value = 0
        for char in str(key):
            value = (value * self.HASH_BASE + ord(char)) % (self.table_size - 1)
        step_size = value + 1  # Ensure step size is not zero
        return step_size

    @property
    def table_size(self) -> int:
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def _hashy_probe(self, key: K, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
        KeyError: When the key is not in the table, but is_insert is False.
        FullError: When a table is full and cannot be inserted.

        Complexity:
            Best Case Complexity: O(1), when the desired position is found immediately.
            Worst Case Complexity: O(N), where N is the table size.
        """
        # Initial position
        position = self.hash(key)

        # Custom logic to be implemented here
        step = self.hash2(key)

        for _ in range(self.table_size):
            item = self.array[position]
            if item is None:
                if is_insert:
                    return position
                else:
                    raise KeyError(f"{key} not found")
            elif item == self.deleted:
                if is_insert:
                    return position
            elif item[0] == key:
                return position
            position = (position + step) % self.table_size
        raise FullError("Hash table is full")
    
    def keys(self) -> list[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res

    def values(self) -> list[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][1])
        return res

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See hashy probe.
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

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self._hashy_probe(key, False)
        return self.array[position][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See hashy probe.
        :raises FullError: when the table cannot be resized further.
        """

        position = self._hashy_probe(key, True)

        if self.array[position] is None:
            self.count += 1

        self.array[position] = (key, data)

        if len(self) > self.table_size * 2 / 3:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) using lazy deletion

        Complexity:
            Best Case Complexity: O(1), when the key is found immediately.
            Worst Case Complexity: O(N), where N is the table size.
        """
        position = self._hashy_probe(key, False)
        self.array[position] = self.deleted
        self.count -= 1

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
        Best Case Complexity: O(N), where N is the table size.
        Worst Case Complexity: O(N)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            raise FullError("Maximum table size reached")
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None and item != self.deleted:
                self[item[0]] = item[1]

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        :complexity: O(N), where N is the table size.
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
