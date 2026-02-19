import requests
from config import NEWS_API_KEY


def get_news(symbol: str) -> list[str]:
    """
    Fetch latest news headlines for an IDX stock.
    Returns list of headline strings.
    """
    try:
        keyword = symbol.replace(".JK", "")

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": keyword,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        }

        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        articles = data.get("articles", [])
        headlines = [a["title"] for a in articles if a.get("title")]

        return headlines

    except Exception as e:
        print(f"[get_news] Error {symbol}: {e}")
        return []