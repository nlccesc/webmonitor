import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup

# fetch webpage content
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
        
# extract price from webpage content
def extract_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_element = soup.find('span', {'class': 'a-offscreen'}) # find price element
    if price_element:
        return price_element.text
    else:
        return None
        
# monitor price
async def monitor(url, interval):
    async with aiohttp.ClientSession() as session:
        last_price = None
        while True:
            content = await fetch(session, url)
            price = extract_price(content)
            if last_price is None:
                print(f'First check for {url}: {price}')
            elif price != last_price:
                print(f'Price changed for {url}: {price}')
            else:
                print(f'No price change for {url}')
            last_price = price
            await asyncio.sleep(interval)

# monitor with 5 sec interval
asyncio.run(monitor('https://linkwhichyouwantomonitor', 5))
