from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def score_news(headlines: list[str]) -> float:
    """
    Score list of headlines using VADER sentiment.
    Returns average compound score between -1 and +1.
    Returns 0.0 (neutral) if no headlines.
    """
    if not headlines:
        return 0.0

    scores = [
        _analyzer.polarity_scores(h)["compound"]
        for h in headlines
        if h and isinstance(h, str)
    ]

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


def normalize_sentiment(raw_score: float) -> float:
    """
    Convert VADER compound score (-1 to +1) to (0 to 1) range.
    Used for combining with other 0-1 scores.
    """
    return (raw_score + 1) / 2