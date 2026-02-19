def combine_scores(tech_signal, ml_confidence, sentiment_score):

    score = 0

    if tech_signal == "BUY":
        score += 0.4

    if tech_signal == "SELL":
        score -= 0.4

    score += ml_confidence * 0.4

    score += sentiment_score * 0.2

    return score