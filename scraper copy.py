import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
from typing import List, Dict, Optional, Tuple
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Constants
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.5
TIMEOUT = 10
MAX_WORKERS = 5

class CartoonScraper:
    def __init__(self):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    @lru_cache(maxsize=100)
    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_search_results(self, query: str) -> List[Dict[str, str]]:
        search_url = f"https://kimcartoon.si/Search/?s={quote(query)}"
        soup = self._make_request(search_url)
        if not soup:
            return []

        cartoons = []
        items = soup.find_all('a', class_='thumb')
        for item in items:
            href = item.get('href')
            title_tag = item.find_next('h2', class_='title')
            if href and title_tag:
                cartoons.append({
                    'title': title_tag.text.strip(),
                    'link': href
                })
        return cartoons

    def _process_episode_link(self, link) -> Optional[Dict]:
        href = link.get('href')
        title = link.text.strip()
        
        season_match = re.search(r'Season-(\d+)', href)
        episode_match = re.search(r'Episode-(\d+)(?:-(\d+))?[^?]*', href)
        
        if not (season_match and episode_match):
            return None

        season = season_match.group(1).zfill(2)
        ep_num = episode_match.group(1)
        
        if episode_match.group(2):
            ep_num = f"{ep_num} & {episode_match.group(2)}"
        ep_num = ep_num.zfill(2)
        
        title_clean = re.sub(r'.*Episode \d+.*?- ', '', title)
        return {
            'season': season,
            'episode_num': ep_num,
            'title': title_clean,
            'link': href
        }

    def get_seasons_and_episodes(self, cartoon_url: str) -> List[Dict]:
        soup = self._make_request(cartoon_url)
        if not soup:
            return []

        episode_links = soup.find_all('a', href=re.compile(r'Season-\d+-Episode'))
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            episodes = list(filter(None, executor.map(self._process_episode_link, episode_links)))
        
        return episodes

def get_user_input(prompt: str, min_val: int, max_val: int) -> Optional[int]:
    while True:
        try:
            choice = int(input(prompt)) - 1
            if min_val <= choice < max_val:
                return choice
            print(f"Please enter a number between {min_val + 1} and {max_val}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            return None

def main():
    scraper = CartoonScraper()
    
    # Get search query
    query = input("Enter cartoon name to search: ").strip()
    if not query:
        print("Query cannot be empty.")
        return

    # Show available cartoons
    cartoons = scraper.get_search_results(query)
    if not cartoons:
        print("No cartoons found.")
        return

    print("\nAvailable cartoons:")
    for i, cartoon in enumerate(cartoons, 1):
        print(f"{i}. {cartoon['title']}")

    # User selects a cartoon
    choice = get_user_input("\nSelect a cartoon (number): ", 0, len(cartoons))
    if choice is None:
        return
    selected_cartoon = cartoons[choice]

    # Get seasons and episodes
    episodes = scraper.get_seasons_and_episodes(selected_cartoon['link'])
    if not episodes:
        print("No episodes found.")
        return

    # Organize episodes by season
    seasons: Dict[str, List[Dict]] = {}
    for ep in episodes:
        season = ep['season']
        seasons.setdefault(season, []).append(ep)

    # Show seasons
    print("\nAvailable seasons:")
    season_list = sorted(seasons.keys())
    for i, season in enumerate(season_list, 1):
        print(f"{i}. Season {season}")

    # User selects a season
    season_choice = get_user_input("\nSelect a season (number): ", 0, len(season_list))
    if season_choice is None:
        return
    selected_season = season_list[season_choice]

    # Show episodes for selected season
    print(f"\nEpisodes in Season {selected_season}:")
    season_episodes = sorted(seasons[selected_season], key=lambda x: x['episode_num'])
    for i, ep in enumerate(season_episodes, 1):
        print(f"{i}. Episode {ep['episode_num']}: {ep['title']}")

    # User selects an episode
    ep_choice = get_user_input("\nSelect an episode (number): ", 0, len(season_episodes))
    if ep_choice is None:
        return
    selected_episode = season_episodes[ep_choice]

    print(f"\nSelected episode link: {selected_episode['link']}")

if __name__ == "__main__":
    main()