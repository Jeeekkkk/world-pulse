import time
import schedule

from services.slack import post_to_slack    
from handlers.news import get_news_summary
from logger import logger

from datetime import datetime
print("Current UTC time:", datetime.utcnow().strftime("%H:%M"))

def send_news_update():
    logger.info("Running scheduled job: sending news summary...")
    try:
        summary = get_news_summary()
        post_to_slack(f"*Daily News Summary:*\n\n{summary}")
        logger.info("Successfully posted news summary to Slack.")
    except Exception as e:
        logger.error("Failed to send news summary in schedule_runner.send_news_update() on Error: %s", str(e))

# Schedule the job (UTC time)
schedule.every().day.at("23:32").do(send_news_update) # 8am PST

logger.info("Scheduler started...")

# Run loop
while True:
    schedule.run_pending()
    time.sleep(30)
