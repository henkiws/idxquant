from data.fetch_stock import get_stock

df = get_stock("BBCA.JK")

print(df.tail())