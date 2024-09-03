#!/usr/bin/env python
"""sub class to form a simple dictionary"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """basic cache class representation"""
    def put(self, key, item):
        """assign to the dictionary self.cache_data the
            item value for the key key
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """getting vaue of a key"""
        if key is None:
            return None
        return self.cache_data.get(key, None)
