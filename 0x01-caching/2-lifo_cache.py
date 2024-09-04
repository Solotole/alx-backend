#!/usr/bin/python3
"""module representing LIFO cache replacement policy"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """class showing LIFO caching"""
    def __init__(self):
        """initialization method"""
        super().__init__()
        self.setkeys = set()
        self.list = []

    def put(self, key, item):
        """assign to the dictionary self.cache_data the
            item value for the key key
        """
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if key not in self.setkeys:
                discarded_key = self.list[len(self.list) - 1]
                del self.list[len(self.list) - 1]
                del self.cache_data[discarded_key]
                print('DISCARD: {}'.format(discarded_key))
        if key is not None and item is not None:
            self.list.append(key)
            self.setkeys.add(key)
            self.cache_data[key] = item

    def get(self, key):
        """method that returns return the value in
            self.cache_data linked to key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)
