#!/usr/bin/env python3
"""LFU Caching replacement policy module"""
import time
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """Class that implements the LFU caching policy."""

    def __init__(self):
        """Initialize the LFUCache class."""
        super().__init__()
        self.access_order = []
        self.key_access_time = {}
        self.frequency_count = {}

    def put(self, key, item):
        """Assign the item value to the key in the cache,
        following LFU policy.
        """
        candidates = []
        if key is None or item is None:
            return
        # Check if cache is full
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if key not in self.cache_data:
                # Find the least frequently used key
                lfu_key = min(self.frequency_count,
                              key=self.frequency_count.get)
                # If multiple keys have the same frequency,
                # evict the least recently used one
                for k, v in self.frequency_count.items():
                    if v == self.frequency_count[lfu_key]:
                        candidates.append(k)
                if len(candidates) > 1:
                    lfu_key = min(candidates, key=self.key_access_time.get)
                # Remove the least frequently used (and least
                # recently used if tied) key
                del self.cache_data[lfu_key]
                del self.key_access_time[lfu_key]
                del self.frequency_count[lfu_key]
                self.access_order.remove(lfu_key)
                print(f"DISCARD: {lfu_key}")

        # Add or update the cache with the new key and item
        self.cache_data[key] = item
        self.key_access_time[key] = time.time()
        self.frequency_count[key] = self.frequency_count.get(key, 0) + 1
        # Update the access order
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

    def get(self, key):
        """Retrieve the value associated with the key in the cache."""
        if key is None or key not in self.cache_data:
            return None
        # Update the access time and frequency for the key
        self.key_access_time[key] = time.time()
        self.frequency_count[key] += 1
        # Move the key to the end of the access order list
        self.access_order.remove(key)
        self.access_order.append(key)

        return self.cache_data.get(key)
