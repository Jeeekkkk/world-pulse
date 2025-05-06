from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=BOT_TOKEN)

@app.message("ping")
def reply_with_pulse(message,say):
    say("WorldPulse is up and listening")

if __name__ == "__main__":
    handler = SocketModeHandler(app,APP_TOKEN)
    handler.start()