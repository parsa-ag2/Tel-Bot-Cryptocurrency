import requests

from config import TWELVE_DATA_API_KEY, TWELVE_DATA_BASE_URL

_coin_cache = None


def find_market(text):

    text = text.strip().lower()

    # اول کریپتو
    coin = find_coin_by_name(text)

    if coin:
        return {
            "type": "crypto",
            "data": coin
        }


    # فارکس
    pairs = get_all_forex_pairs()

    query = text.upper().replace(" ", "")

    if query in pairs:
        return {
            "type": "forex",
            "data": query
        }


    # ارز کوتاه مثل EUR
    pair = query + "/USD"

    if pair in pairs:
        return {
            "type": "forex",
            "data": pair
        }


    # کالاها
    commodities = {
        "gold": "GOLD",
        "طلا": "GOLD",
        "silver": "SILVER",
        "نقره": "SILVER",
        "oil": "BRENT",
        "نفت": "BRENT",
    }


    if text in commodities:
        return {
            "type": "commodity",
            "data": commodities[text]
        }


    return None

def get_all_coins():
    global _coin_cache

    if _coin_cache is None:
        url = "https://api.coingecko.com/api/v3/coins/list"
        _coin_cache = requests.get(url, timeout=10).json()

    return _coin_cache

def find_coin_by_name(name):

    name = name.strip().lower()

    coins = get_all_coins()

    for coin in coins:

        if coin["name"].lower() == name:
            return coin

    return None



def search_coins(query):

    query = query.strip()

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


        # اولویت بندی نتایج
        coins.sort(
            key=lambda c: (
                c["symbol"].lower() != query_lower,
                c["name"].lower() != query_lower,
                c.get("market_cap_rank") or 999999
            )
        )


        # اگر اسم کامل بود فقط همان ارز
        for coin in coins:

            if coin["name"].lower() == query_lower:

                return [
                    coin
                ]


        return coins


    except Exception as e:

        print(
            "SEARCH ERROR:",
            e
        )

        return []

# ---------- کریپتو ----------

def get_price(coin_id):

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}"
        "&vs_currencies=usd"
        "&include_24hr_change=true"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "usd": data[coin_id]["usd"],
            "change": data[coin_id]["usd_24h_change"],
        }

    except Exception:
        return None


# ---------- تتر تومان والکس ----------

def get_usdt_toman():

    url = "https://api.wallex.ir/v1/markets"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()


        markets = data["result"]["symbols"]


        usdt = markets.get("USDTTMN")


        if not usdt:
            return None


        price = usdt["stats"]["lastPrice"]


        return float(price)



    except requests.exceptions.RequestException as e:

        print(
            "WALLEX ERROR:",
            e
        )

        return None
# ---------- فارکس Twelve Data ----------



_forex_cache = None


def get_all_forex_pairs():

    global _forex_cache

    if _forex_cache is not None:
        return _forex_cache


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

            symbol = item.get("symbol")

            if symbol:
                pairs.append(symbol)


        _forex_cache = pairs

        return pairs


    except Exception as e:

        print(
            "FOREX LIST ERROR:",
            e
        )

        return []



def get_forex_price(pair):

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



        return {
            "symbol": pair,
            "price": float(data["close"]),
            "change": float(
                data.get(
                    "percent_change",
                    0
                )
            )
        }



    except Exception as e:

        print(
            "FOREX PRICE ERROR:",
            e
        )

        return None
    
# ---------- شاخص ها  ----------

COMMODITIES = {
    "BRENT": "BZ=F",      # نفت برنت
    "WTI": "CL=F",        # نفت خام آمریکا
    "GOLD": "GC=F",       # طلا
    "SILVER": "SI=F",     # نقره
    "NATGAS": "NG=F",     # گاز طبیعی
    "COPPER": "HG=F",     # مس
}


def get_commodity_price(symbol):

    yahoo_symbol = COMMODITIES.get(symbol)

    if not yahoo_symbol:
        return None

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        print("YAHOO STATUS:", response.status_code)

        response.raise_for_status()

        result = response.json()["chart"]["result"]

        if not result:
            return None

        meta = result[0]["meta"]

        return {
            "price": meta.get("regularMarketPrice"),
            "change": meta.get(
                "regularMarketChangePercent",
                0
            )
        }

    except Exception as e:
        print("COMMODITY ERROR:", e)
        return None