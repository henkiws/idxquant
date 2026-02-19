def rank_stocks(results):

    return sorted(results,key=lambda x:x["confidence"],reverse=True)
