from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os

from services.slack import post_to_slack    
from handlers.news import get_news_summary

load_dotenv()
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=BOT_TOKEN)

@app.message("news")
def handle_news(message,say):
    summary = get_news_summary()
    say(f"*News Summary:*\n\n{summary}")

if __name__ == "__main__":
    handler = SocketModeHandler(app,APP_TOKEN)
    handler.start()