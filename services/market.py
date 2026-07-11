import requests

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
# ---------- فارکس ----------


FOREX_SYMBOLS = {
    "EUR/USD": ("EUR", "USD"),
    "GBP/USD": ("GBP", "USD"),
    "USD/JPY": ("USD", "JPY"),
    "AUD/USD": ("AUD", "USD"),
    "USD/CAD": ("USD", "CAD"),
    "NZD/USD": ("NZD", "USD"),
    "EUR/JPY": ("EUR", "JPY"),
    "GBP/JPY": ("GBP", "JPY"),
}


def get_forex_price(pair):

    if pair not in FOREX_SYMBOLS:
        return None

    base, quote = FOREX_SYMBOLS[pair]

    url = f"https://api.frankfurter.app/latest?from={base}&to={quote}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "price": float(data["rates"][quote]),
            "change": 0.0
        }

    except Exception as e:
        print(e)
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