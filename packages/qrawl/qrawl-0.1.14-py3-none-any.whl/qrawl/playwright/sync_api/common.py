# Standard Libraries
import time

# Third-Party Libraries
from playwright.sync_api import Page


def delay_request(time_of_last_request: float, delay: float = 1):
    """
    To prevent sending too many requests to server at once.
    """
    elapsed_time = time.time() - time_of_last_request
    if elapsed_time < delay:
        time.sleep()
    return time.time()


def get_ip(page: Page):
    page.goto("https://www.whatismyip.com/")
    ip_element = page.wait_for_selector(".ip-address")
    ip_address = ip_element.text_content()
    return ip_address.strip()
