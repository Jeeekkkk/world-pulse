import time
import schedule
import os
from services.slack import post_to_slack    
from handlers.news import get_news_summary
from logger import logger
from zoneinfo import ZoneInfo
from datetime import datetime, time as dtime, timedelta
print("Current UTC time:", datetime.utcnow().strftime("%H:%M"))

def send_news_update():
    logger.info("Running scheduled job: sending news summary...")
    try:
        summary = get_news_summary()
        post_to_slack(f"*Daily News Summary:*\n\n{summary}")
        logger.info("Successfully posted news summary to Slack.")
    except Exception as e:
        logger.error("Failed to send news summary in schedule_runner.send_news_update() on Error: %s", str(e))

# Schedule the job (User local time converted to UTC)
USER_TIMEZONE = os.getenv("USER_TIMEZONE", "America/Los_Angeles")
POST_HOUR = int(os.getenv("POST_HOUR", 7))
POST_MINUTE = int(os.getenv("POST_MINUTE", 0))

local_zone = ZoneInfo(USER_TIMEZONE)
utc_zone = ZoneInfo("UTC")
local_target_time = dtime(hour=POST_HOUR, minute=POST_MINUTE)
local_dt = datetime.combine(datetime.today(), local_target_time, tzinfo=local_zone)
utc_dt = local_dt.astimezone(utc_zone)
target_time = utc_dt.strftime("%H:%M")
schedule.every().day.at(target_time).do(send_news_update)

logger.info("Scheduler started... target time is %s", target_time)
logger.debug("Scheduled jobs: %s", schedule.jobs)

# Run loop
while True:
    schedule.run_pending()
    time.sleep(30)
    logger.debug("Checking schedule at %s", datetime.utcnow().strftime("%H:%M:%S"))
