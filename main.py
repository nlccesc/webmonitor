import asyncio
import sys
import logging
from monitor import monitor_price

# init
logging.basicConfig(filename='web_monitor.log', level=logging.INFO)


async def main():
    urls = sys.argv[1:] if len(sys.argv) > 1 else ['https://www.amazon.sg/GeForce-Founders-Graphics-GDDR6X-Titanium/dp/B0BLCBLCDR']
    interval = 5
    await asyncio.gather(*(monitor_price(url, interval) for url in urls))

# start web monitor
if __name__ == "__main__":
    asyncio.run(main())