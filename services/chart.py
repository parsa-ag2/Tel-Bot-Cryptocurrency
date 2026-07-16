import requests
import matplotlib.pyplot as plt


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
            "vs_currency":"usd",
            "days":days[timeframe]
        },
        timeout=10
    )


    data=response.json()


    prices = [
        x[1]
        for x in data["prices"]
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


    file = "chart.png"


    plt.savefig(
        file
    )


    plt.close()


    return file