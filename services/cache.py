import time


CACHE_TIME = 100 


_cache = {}



def get_cache(key):

    if key not in _cache:
        return None


    data, timestamp = _cache[key]


    if time.time() - timestamp > CACHE_TIME:

        del _cache[key]
        return None


    return data



def set_cache(key, data):

    _cache[key] = (
        data,
        time.time()
    )


def clear_cache():

    _cache.clear()