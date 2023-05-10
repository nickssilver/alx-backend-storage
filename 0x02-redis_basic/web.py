#!/usr/bin/env python3
"""Module tracks how many times a particular URL was accessed"""
import redis
import requests
from typing import Callable
from functools import wraps


def count(method: Callable):
    '''track how many times a particular URL was accessed'''
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        '''wrap the decorated function and return the wrapper'''
        r.incr(f"count:{url}")
        exp_count = r.get(f"cached:{url}")
        if exp_count:
            return exp_count.decode('utf-8')
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count
def get_page(url: str) -> str:
    '''uses the requests module to obtain the HTML content'''
    return requests.get(url).text
