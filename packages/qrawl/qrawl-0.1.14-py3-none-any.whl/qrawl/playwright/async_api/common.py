# Standard Libraries
import asyncio
import time

# Third-Party Libraries
from playwright.async_api import Page


async def delay_request(time_of_last_request: float, delay: float = 1):
    """
    To prevent sending too many requests to server at once.
    """
    elapsed_time = time.time() - time_of_last_request
    if elapsed_time < delay:
        await asyncio.sleep(delay - elapsed_time)
    return time.time()


async def get_ip(page: Page):
    await page.goto("https://www.whatismyip.com/")
    ip_element = await page.wait_for_selector(".ip-address")
    ip_address = await ip_element.text_content()
    return ip_address.strip()
