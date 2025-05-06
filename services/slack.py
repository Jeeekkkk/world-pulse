import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from logger import logger

load_dotenv()
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DEFAULT_CHANNEL = "#world-pulse"

slack_client = WebClient(token=BOT_TOKEN)

def post_to_slack(text, channel=DEFAULT_CHANNEL):
    try:
        response = slack_client.chat_postMessage(channel=channel,text=text)
        if response["ok"]:
            logger.info("Successfully sent message")
        return response
    except Exception as e:
        logger.error("Slack API in services/slack.post_to_slack() on Error:", str(e))
        from logger import logger
        logger.info("File ran successfully: 'services/slack.py")