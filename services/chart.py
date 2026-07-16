import requests
import matplotlib.pyplot as plt
import uuid


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


    return None





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

        f"https://api.coingecko.com/api/v3/"

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



    plt.figure(
        figsize=(8,4)
    )



    plt.plot(
        prices
    )



    plt.title(
        f"{coin_id} {timeframe}"
    )



    file = f"chart_{uuid.uuid4().hex}.png"



    plt.savefig(
        file,
        bbox_inches="tight"
    )



    plt.close()



    return file