import time


CACHE_TIME = 100


_cache = {}



def get_cache(key):

    if key not in _cache:
        return None


    data, timestamp, expire = _cache[key]


    if time.time() - timestamp > expire:

        del _cache[key]

        return None


    return data





def set_cache(
    key,
    data,
    expire=CACHE_TIME
):

    _cache[key] = (

        data,

        time.time(),

        expire

    )





def clear_cache():

    _cache.clear()