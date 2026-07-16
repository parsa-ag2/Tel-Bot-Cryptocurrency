import requests

from config import TWELVE_DATA_API_KEY, TWELVE_DATA_BASE_URL
from services.cache import (
    get_cache,
    set_cache
)



# =====================
# Crypto Aliases
# =====================

CRYPTO_ALIASES = {

    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "bitcoin": "bitcoin",
    "btc": "bitcoin",

    "اتریوم": "ethereum",
    "ethereum": "ethereum",
    "eth": "ethereum",

}


# =====================
# Forex Aliases
# =====================

FOREX_ALIASES = {

    "یورو": "EUR/USD",
    "eur": "EUR/USD",

    "پوند": "GBP/USD",
    "gbp": "GBP/USD",

    "ین": "JPY/USD",
    "jpy": "JPY/USD",

}


# =====================
# Commodity Aliases
# =====================

COMMODITY_ALIASES = {

    "طلا": "GOLD",
    "gold": "GOLD",
    "xau": "GOLD",
    "xauusd": "GOLD",

    "نقره": "SILVER",
    "silver": "SILVER",

    "نفت": "BRENT",
    "oil": "BRENT",

}


# =====================
# USD Aliases
# =====================

USD_ALIASES = {

    "دلار": "USD",
    "دلار آمریکا": "USD",
    "usd": "USD",
    "تتر": "USD",
    "usdt": "USD",

}

def find_market(text):

    text = text.strip().lower()


    # =====================
    # USD
    # =====================

    if text in USD_ALIASES:

        return {
            "type": "usd",
            "data": USD_ALIASES[text]
        }



    # =====================
    # Commodity
    # =====================

    if text in COMMODITY_ALIASES:

        return {
            "type": "commodity",
            "data": COMMODITY_ALIASES[text]
        }



    # =====================
    # Forex
    # =====================

    if text in FOREX_ALIASES:

        return {
            "type": "forex",
            "data": FOREX_ALIASES[text]
        }



    # =====================
    # Crypto Alias
    # =====================

    if text in CRYPTO_ALIASES:

        coin_id = CRYPTO_ALIASES[text]

        coins = get_all_coins()

        for coin in coins:

            if coin["id"] == coin_id:

                return {
                    "type": "crypto",
                    "data": coin
                }


    # =====================
    # بعد از اینجا سرچ عمومی
    # =====================


    coin = find_coin_by_name(text)

    if coin:
        return {
            "type": "crypto",
            "data": coin
        }


    return None

_coin_cache = None



def get_all_coins():

    global _coin_cache


    if _coin_cache is not None:
        return _coin_cache


    cache_key = "all_crypto_coins"


    cached = get_cache(cache_key)

    if cached:
        _coin_cache = cached
        return cached



    url = "https://api.coingecko.com/api/v3/coins/list"


    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()


        coins = response.json()


        _coin_cache = coins


        set_cache(
            cache_key,
            coins,
            300   # ۵ دقیقه
        )


        return coins



    except Exception as e:

        print(
            "COINS LIST ERROR:",
            e
        )

        return []



def find_coin_by_name(name):

    name = name.strip().lower()


    coins = get_all_coins()


    for coin in coins:

        if coin["name"].lower() == name:

            return coin


    return None


def search_coins(query):

    query = query.strip().lower()


    # اول alias ها
    if query in CRYPTO_ALIASES:

        coin_id = CRYPTO_ALIASES[query]

        coins = get_all_coins()

        for coin in coins:

            if coin["id"] == coin_id:
                return [coin]



    cache_key = f"coin_search_{query}"


    cached = get_cache(cache_key)

    if cached:
        return cached



    url = "https://api.coingecko.com/api/v3/search"


    try:

        response = requests.get(
            url,
            params={
                "query": query
            },
            timeout=10
        )


        response.raise_for_status()


        coins = response.json().get(
            "coins",
            []
        )



        if not coins:
            return []



        query_lower = query.lower()



        coins.sort(
            key=lambda c: (
                c["symbol"].lower() != query_lower,
                c["name"].lower() != query_lower,
                c.get("market_cap_rank") or 999999
            )
        )



        result = coins[:5]



        set_cache(
            cache_key,
            result,
            300
        )


        return result



    except Exception as e:

        print(
            "SEARCH ERROR:",
            e
        )

        return []

# ---------- کریپتو ----------

def get_price(coin_id):

    cache_key = f"crypto_price_{coin_id}"

    # اول کش
    cached = get_cache(cache_key)

    if cached:
        return cached


    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}"
        "&vs_currencies=usd"
        "&include_24hr_change=true"
    )


    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()


        result = {

            "usd": data[coin_id]["usd"],

            "change": data[coin_id]["usd_24h_change"]

        }


        
        set_cache(
            cache_key,
            result,
            100
        )


        return result



    except Exception as e:

        print(
            "CRYPTO PRICE ERROR:",
            e
        )

        return None



# ---------- تتر تومان والکس ----------

def get_usdt_toman():

    cache_key = "usdt_toman_price"


    # اول کش
    cached = get_cache(cache_key)

    if cached:
        return cached



    url = "https://api.wallex.ir/v1/markets"


    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()


        data = response.json()


        markets = data["result"]["symbols"]


        usdt = markets.get(
            "USDTTMN"
        )


        if not usdt:
            return None



        price = float(
            usdt["stats"]["lastPrice"]
        )


        
        set_cache(
            cache_key,
            price,
            100
        )


        return price



    except Exception as e:

        print(
            "WALLEX ERROR:",
            e
        )

        return None
# ---------- فارکس Twelve Data ----------


_forex_cache = None


def get_all_forex_pairs():

    cache_key = "forex_pairs"


    # اول کش
    cached = get_cache(cache_key)

    if cached:
        return cached



    url = f"{TWELVE_DATA_BASE_URL}/forex_pairs"


    params = {
        "apikey": TWELVE_DATA_API_KEY
    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        response.raise_for_status()


        data = response.json()


        pairs = []


        for item in data.get("data", []):

            symbol = item.get(
                "symbol"
            )

            if symbol:
                pairs.append(symbol)



       
        set_cache(
            cache_key,
            pairs,
            100
        )


        return pairs



    except Exception as e:

        print(
            "FOREX LIST ERROR:",
            e
        )

        return []


def get_forex_price(pair):

    cache_key = f"forex_price_{pair}"


    cached = get_cache(cache_key)

    if cached:
        return cached



    url = f"{TWELVE_DATA_BASE_URL}/quote"


    params = {
        "symbol": pair,
        "apikey": TWELVE_DATA_API_KEY
    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        response.raise_for_status()


        data = response.json()



        if "close" not in data:

            print(
                "TWELVE ERROR:",
                data
            )

            return None



        result = {

            "symbol": pair,

            "price": float(
                data["close"]
            ),

            "change": float(
                data.get(
                    "percent_change",
                    0
                )
            )

        }



        # کش کوتاه برای قیمت
        set_cache(
            cache_key,
            result,
            60
        )


        return result



    except Exception as e:

        print(
            "FOREX PRICE ERROR:",
            e
        )

        return None
    


# ---------- Commodities Twelve Data ----------


COMMODITY_SYMBOLS = {

    "GOLD": "XAU/USD",
    "SILVER": "XAG/USD",
    "BRENT": "BRENT",
    "WTI": "WTI",
    "COPPER": "COPPER",
    "NATGAS": "NATGAS"

}



def get_commodity_price(symbol):

    cache_key = f"commodity_price_{symbol}"


    # اول کش
    cached = get_cache(cache_key)

    if cached:
        return cached



    pair = COMMODITY_SYMBOLS.get(symbol)


    if not pair:
        return None



    url = f"{TWELVE_DATA_BASE_URL}/quote"


    params = {

        "symbol": pair,

        "apikey": TWELVE_DATA_API_KEY

    }



    try:

        response = requests.get(

            url,

            params=params,

            timeout=10

        )


        response.raise_for_status()


        data = response.json()



        if "close" not in data:

            print(

                "COMMODITY ERROR:",

                data

            )

            return None




        result = {


            "price": float(

                data["close"]

            ),


            "change": float(

                data.get(

                    "percent_change",

                    0

                )

            )

        }



        # کش ۱ دقیقه
        set_cache(

            cache_key,

            result,

            60

        )



        return result




    except Exception as e:


        print(

            "COMMODITY ERROR:",

            e

        )


        return None
