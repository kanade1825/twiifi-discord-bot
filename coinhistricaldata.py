import requests


async def real_time_price():
    URL = "https://api.coingecko.com/api/v3"
    #/simple/price (価格を取得)
    endpoint = "/simple/price"
    url = URL + endpoint
    params = {"ids":"twitfi","vs_currencies":"usd"}
    response = requests.request("GET", url, params=params)
    r = response.json()
    print(r["twitfi"]["usd"])

    price = str(r["twitfi"]["usd"])

    return price

