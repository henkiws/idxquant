from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def score_news(news):

    if not news:
        return 0

    scores = []

    for n in news:

        s = analyzer.polarity_scores(n)["compound"]

        scores.append(s)

    return sum(scores)/len(scores)
