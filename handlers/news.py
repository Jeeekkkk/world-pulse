import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()
NEWSORG_API_KEY = os.getenv("NEWSORG_TOKEN") # https://newsapi.org/
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client (new SDK version)
client = OpenAI(api_key=OPENAI_API_KEY)

# Fetch top headlines from curated sources
def fetch_headlines():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "language": "en",
        "pageSize": 50,
        "sources": "associated-press,npr,reuters,politico,bbc-news",
    }
    headers = {"Authorization": NEWSORG_API_KEY}
    response = requests.get(url,params=params,headers=headers)
    return response.json().get("articles", [])

# Filters articles published on the previous day
def filter_by_yesterday(articles):
    utc_now = datetime.utcnow()
    yesterday = utc_now - timedelta(days=1)
    return [
        a for a in articles
        if 'publishedAt' in a and
        yesterday.date() == datetime.fromisoformat(a['publishedAt'].replace('Z','+00:00')).date()
    ]

# Summarizes filtered articles using OpenAI GPT
def summarize_articles_with_gpt(articles):
    if not articles:
        return "No news articles found for yesterday."

    content = "\n".join(
    f"- [{a['source']['name']}] {a['title']}" for a in articles if a.get("title")
    )


    today = datetime.utcnow().strftime("%B %d, %Y")

    prompt = (
    f"You are a helpful and unbiased news summarizer. Today is {today}.\n"
    f"Do not invent facts or add outside context. Only summarize what is in the list of headlines below.\n\n"
    f"Select the 5 most important U.S. news stories and 5 most important international news stories.\n\n"
    f"Format your response exactly like this:\n"
    f"**U.S. News:**\n"
    f"1. *[Source] Title* — One-sentence summary.\n"
    f"...\n\n"
    f"**International News:**\n"
    f"1. *[Source] Title* — One-sentence summary.\n"
    f"...\n\n"
    f"Here is the list of headlines:\n\n"
    f"{content}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful and unbiased news summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=600
    )

    return response.choices[0].message.content

def get_news_summary():
    articles = fetch_headlines()
    filtered = filter_by_yesterday(articles)
    return summarize_articles_with_gpt(filtered)

# Script entry point for testing
if __name__ == "__main__":
    summary = get_news_summary()

    with open("news_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("News summary saved to news_summary.txt")
