import time
import schedule

from services.slack import post_to_slack    
from handlers.news import get_news_summary

from datetime import datetime
print("Current UTC time:", datetime.utcnow().strftime("%H:%M"))

def send_news_update():
    print("Running scheduled job: sending news summary...")
    summary = get_news_summary()
    post_to_slack(f"*Daily News Summary:*\n\n{summary}")

# Schedule the job (UTC time, adjust as needed)
schedule.every().day.at("21:25").do(send_news_update) # 8am PST

print("Scheduler started...")

# Run loop
while True:
    schedule.run_pending()
    time.sleep(1)