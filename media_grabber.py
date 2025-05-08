import requests

headers = {
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua": '"Not.A/Brand";v="99", "Chromium";v="136"',
    "sec-ch-ua-mobile": "?0",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...Safari/537.36",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "dnt": "1",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://kimcartoon.si",
    "referer": "https://kimcartoon.si/Cartoon/Ben-10-Ultimate-Alien.79888/Season-03-Episode-18-The-Enemy-of-My-Enemy?id=1207",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cookie": "uname=Dhairya3391; PHPSESSID=6dtvao27ahba8llt5rbrr67837; view-68=true",
}

data = {"episode_id": "1207"}

r = requests.post(
    "https://kimcartoon.si/ajax/anime/load_episodes_v2?s=tserver",
    headers=headers,
    data=data,
)

# Extract the embedded player link
from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text, "html.parser")
iframe = soup.find("iframe")
if iframe:
    video_url = iframe.get("src")
    cleaned = video_url.replace('\\', '').strip('"')
    print("🔗 Clean Video Player URL:", cleaned)

else:
    print("❌ Could not find iframe in response.")
