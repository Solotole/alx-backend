#!/usr/bin/env python3
"""pagination using page indexes and page size"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """index pagination"""
    start: int = (page - 1) * page_size
    end: int = page * page_size
    # new_tuple = tuple(start, end)
    return (start, end)
