import requests

from config import TWELVE_DATA_API_KEY, TWELVE_DATA_BASE_URL

_coin_cache = None

def get_all_coins():
    global _coin_cache

    if _coin_cache is None:
        url = "https://api.coingecko.com/api/v3/coins/list"
        _coin_cache = requests.get(url, timeout=10).json()

    return _coin_cache


def find_coin(query):

    query = query.lower().strip()

    coins = get_all_coins()


    # exact id
    for coin in coins:
        if coin["id"].lower() == query:
            return coin


    # exact name
    for coin in coins:
        if coin["name"].lower() == query:
            return coin


    # symbol matches
    matches = []

    for coin in coins:
        if coin["symbol"].lower() == query:
            matches.append(coin)


    if not matches:
        return None


    # پیدا کردن کوینی که قیمت واقعی دارد
    for coin in matches:

        price = get_price(coin["id"])

        if price and price["usd"] > 0:
            return coin


    return matches[0]



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