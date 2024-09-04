#!/usr/bin/env python3
"""LRU Caching replacement policy module"""
import time
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """Class that implements the LRU caching policy."""

    def __init__(self):
        """Initialize the LRUCache class."""
        super().__init__()
        self.access_order = []
        self.key_access_time = {}

    def put(self, key, item):
        """Assign the item value to the key in the cache, following LRU policy
        """
        if key is None or item is None:
            return

        # Checking if cache is full
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # deleting the least recently used item
            if key not in self.cache_data:
                # Find the key with the oldest access time
                lru_key = min(self.key_access_time,
                              key=self.key_access_time.get)
                # Remove it from the cache
                del self.cache_data[lru_key]
                del self.key_access_time[lru_key]
                self.access_order.remove(lru_key)
                print(f"DISCARD: {lru_key}")
        # Add or update the cache with the new key and item
        self.cache_data[key] = item
        self.key_access_time[key] = time.time()
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

    def get(self, key):
        """Retrieve the value associated with the key in the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update the access time for the key
        self.key_access_time[key] = time.time()
        # Move the key to the end of the access order list
        self.access_order.remove(key)
        self.access_order.append(key)

        return self.cache_data.get(key)
