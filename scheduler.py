import schedule
import time

from main import run

schedule.every().day.at("16:00").do(run)

print("IDXQuantBot Hedge Fund Version Running...")

while True:

    schedule.run_pending()

    time.sleep(60)