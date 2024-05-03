# List of common User-Agent substrings used by bots
from flask import request

known_bots = [
    "bot", "crawl", "slurp", "spider", "curl", "wget", "python-requests",
    "httpclient", "phpcrawl", "bingbot", "yandex", "facebookexternalhit"
]

def is_bot():
    user_agent = request.headers.get('User-Agent', '').lower()
    if any(bot in user_agent for bot in known_bots):
        return True
    # Check for necessary headers often missing in bot requests
    necessary_headers = ["Accept", "Content-Type"]
    if not all(header in request.headers for header in necessary_headers):
        return True
    return False
