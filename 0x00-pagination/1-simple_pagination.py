#!/usr/bin/env python3
import csv
import math
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """getting dataset in the range"""
        # asserting for type int and positive arguments
        assert type(page) == int
        assert type(page_size) == int
        assert page > 0
        assert page_size > 0
        try:
            # tuple of pagination
            index = self.index_range(page, page_size)
            # accessing data from the csv file
            data = self.dataset()
            # accessing data between the tuple indices
            paginated_data = data[index[0]:index[1]]
        # incase out of range due to large arguments size
        except IdexError:
            # return empty list if IndexError raised
            return []
        return list(paginated_data)
    
    def index_range(self, page: int, page_size: int) -> Tuple:
        """index pagination"""
        start: int = (page - 1) * page_size
        end: int = page * page_size
        # new_tuple = tuple(start, end)
        return (start, end)