import aiohttp
from bs4 import BeautifulSoup
import logging


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logging.error(f"An error occurred while fetching {url}: {e}")
        return None


def extract_price(html):
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    price_element = soup.find('span', {'class': 'a-offscreen'})  # find price element
    return price_element.text if price_element else None