import requests
import matplotlib.pyplot as plt
import uuid

from config import (
    TWELVE_DATA_API_KEY,
    TWELVE_DATA_BASE_URL
)


# =========================
# تبدیل تایم فریم
# =========================

def convert_timeframe(tf):

    return {

        "5m": "5min",

        "15m": "15min",

        "30m": "30min",

        "60m": "1h"

    }.get(
        tf,
        "15min"
    )



# =========================
# Main Chart Router
# =========================


def create_chart(
    market_type,
    symbol,
    timeframe
):


    if market_type == "crypto":

        return create_crypto_chart(
            symbol,
            timeframe
        )


    elif market_type in [
        "forex",
        "commodity",
        "index"
    ]:

        return create_twelve_chart(
            symbol,
            timeframe
        )


    return None




# =========================
# Crypto Chart
# =========================


def create_crypto_chart(
    coin_id,
    timeframe
):


    days = {

        "5m": "1",

        "15m": "1",

        "30m": "1",

        "60m": "7"

    }



    url = (
        "https://api.coingecko.com/api/v3/"
        f"coins/{coin_id}/market_chart"
    )


    response = requests.get(

        url,

        params={

            "vs_currency": "usd",

            "days": days.get(
                timeframe,
                "1"
            )

        },

        timeout=10

    )


    response.raise_for_status()


    data = response.json()



    prices = [

        item[1]

        for item in data["prices"]

    ]



    return save_chart(

        prices,

        f"{coin_id} {timeframe}"

    )





# =========================
# Forex / Commodity / Index
# Twelve Data
# =========================


def create_twelve_chart(
    symbol,
    timeframe
):


    interval = convert_timeframe(
        timeframe
    )



    url = (
        f"{TWELVE_DATA_BASE_URL}/time_series"
    )



    params = {

        "symbol": symbol,

        "interval": interval,

        "outputsize": 100,

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



        values = data.get(
            "values"
        )



        if not values:

            print(
                "NO CHART DATA:",
                data
            )

            return None



        values.reverse()



        prices = [

            float(
                x["close"]
            )

            for x in values

        ]



        return save_chart(

            prices,

            f"{symbol} {timeframe}"

        )



    except Exception as e:


        print(
            "TWELVE CHART ERROR:",
            e
        )


        return None





# =========================
# Save PNG
# =========================


def save_chart(
    prices,
    title
):


    plt.figure(

        figsize=(8,4)

    )


    plt.plot(
        prices
    )


    plt.title(
        title
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Price"
    )



    file = (

        f"chart_"
        f"{uuid.uuid4().hex}"
        ".png"

    )



    plt.savefig(

        file,

        bbox_inches="tight"

    )



    plt.close()



    return file