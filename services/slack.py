import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DEFAULT_CHANNEL = "#world_pulse"

slack_client = WebClient(token=BOT_TOKEN)

def post_to_slack(text, channel=DEFAULT_CHANNEL):
    try:
        slack_client.chat_postMessage(channel=channel,text=text)
        if not response["ok"]:
            print("Failed to send message:", response["error"])
        return response
    except Exception as e:
        print("Slack API error:", str(e))
    