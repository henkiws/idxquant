import requests
from config import NEWS_API_KEY

def get_news(symbol):

    keyword = symbol.replace(".JK","")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    r = requests.get(url, params=params)

    data = r.json()

    articles = []

    if "articles" in data:

        for article in data["articles"]:

            articles.append(article["title"])

    return articles
