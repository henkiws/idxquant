def calculate_score(ml, sentiment):

    score = ml*0.7 + sentiment*0.3

    if score > 0.6:
        signal="BUY"
    elif score < 0.4:
        signal="SELL"
    else:
        signal="HOLD"

    return score, signal
