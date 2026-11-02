import os
import requests
import time

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

API = f"https://api.telegram.org/bot{TOKEN}"

CATEGORIES = {
    "Boys Photos": "boys portrait photography",
    "Girls Photos": "girls portrait photography",
    "Birthday Photos": "birthday photography"
}

def send_message(text):
    requests.post(
        f"{API}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )

def search_images(query):
    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": 2,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    headers = {
        "User-Agent": "PromptZenAutomation/1.0 (research bot)"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        raise Exception(
            f"Wikimedia returned invalid response: "
            f"{response.text[:300]}"
        )

    return data.get("query", {}).get("pages", {}).values()

    response = requests.get(url, params=params).json()
    return response.get("query", {}).get("pages", {}).values()

for category, query in CATEGORIES.items():

    send_message(f"Research Category: {category}")

    for item in search_images(query):

        image = item.get("imageinfo", [{}])[0].get("url")

        if not image:
            continue

        message = (
            f"Category: {category}\n\n"
            f"Image URL: {image}\n\n"
            f"Short Prompt: /portraitstyle\n\n"
            f"Detailed Prompt: Create a beautiful, "
            f"high-quality {query}, professional composition."
        )

        requests.post(
            f"{API}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "photo": image,
                "caption": message[:1000]
            }
        )

        time.sleep(2)

send_message("Research Test Completed!")
