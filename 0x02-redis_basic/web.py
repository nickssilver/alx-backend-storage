#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import time
from functools import wraps

def get_page(url: str) -> str:
    cache_key = f"count:{url}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result
    response = requests.get(url)
    content = response.content.decode('utf-8')
    cache.set(cache_key, content, expire=10)
    return content

class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        if key not in self.cache:
            return None
        value, expiration_time = self.cache[key]
        if expiration_time is not None and time.time() > expiration_time:
            del self.cache[key]
            return None
        return value

    def set(self, key, value, expire=None):
        if expire is not None:
            expiration_time = time.time() + expire
        else:
            expiration_time = None
        self.cache[key] = (value, expiration_time)

cache = Cache()

def cached(expiration_time=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"count:{args[0]}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, expire=expiration_time)
            return result
        return wrapper
    return decorator

@cached(expiration_time=10)
def get_page_cached(url: str) -> str:
    response = requests.get(url)
    content = response.content.decode('utf-8')
    return content
