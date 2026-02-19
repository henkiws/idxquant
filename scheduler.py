"""
Runs the bot automatically every weekday at 16:10 WIB
(10 minutes after IDX market close at 16:00).
"""

import schedule
import time
from datetime import datetime

from main import run


def job():
    # only run on weekdays
    if datetime.now().weekday() < 5:  # 0=Mon, 4=Fri
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Running scheduled scan...")
        run()
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Weekend — skipping.")


schedule.every().day.at("16:10").do(job)

print("IDXQuantBot Scheduler started.")
print("Will run every weekday at 16:10 WIB.\n")

while True:
    schedule.run_pending()
    time.sleep(60)