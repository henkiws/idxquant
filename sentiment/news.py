import requests
from config import NEWS_API_KEY


def get_news(symbol):

    name = symbol.replace(".JK","")

    url = f"https://newsapi.org/v2/everything?q={name}&apiKey={NEWS_API_KEY}"

    r = requests.get(url)

    articles = r.json().get("articles", [])

    return [a["title"] for a in articles[:5]]
