import aiohttp
import asyncio
from fetch import fetch, extract_price
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = 'your-email@gmail.com'
GMAIL_PASSWORD = 'your-password'

# Send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USERNAME
    msg['To'] = GMAIL_USERNAME
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(GMAIL_USERNAME, GMAIL_USERNAME, text)
    server.quit()

# Monitor price
async def monitor_price(url, interval):
    async with aiohttp.ClientSession() as session:
        last_price = None
        while True:
            content = await fetch(session, url)
            price = extract_price(content)
            if price is None:
                logging.error(f"Failed to fetch or extract price for {url}")
            elif last_price is None:
                logging.info(f'First check for {url}: {price}')
            elif price != last_price:
                logging.info(f'Price changed for {url}: {price}')
                send_email(f'Price changed for {url}', f'New price: {price}')
            else:
                logging.info(f'No price change for {url}')
            last_price = price
            await asyncio.sleep(interval)