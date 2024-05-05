# Third-Party Libraries
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, BrowserContext, Page
from playwright.sync_api import Route, Request

# Local Libraries
from qrawl import add_params_to_url, get_cookie_header, get_random_user_agent


def get_new_context(
    browser: Browser,
    user_agent: str = "",
    headers: dict | None = None,
    cookies: dict | None = None,
) -> BrowserContext:
    # Get random user agent if not defined
    if user_agent == "":
        user_agent = get_random_user_agent()

    context = browser.new_context(user_agent=user_agent)

    h = {
        # Define default headers here
        "referer": "https://www.google.com/",
        "user-agent": user_agent,
    }

    # Add additional headers
    if headers is not None:
        h.update(headers)

    # Add cookies
    if cookies is not None:
        context.add_cookies(cookies)
        h.update({"cookies": get_cookie_header(cookies)})

    context.set_extra_http_headers(h)

    return context


def get_new_page(context: BrowserContext) -> Page:
    page = context.new_page()

    # Set webdriver to false automatically for added stealth
    set_webdriver_to_false(page)
    return page


def set_webdriver_to_false(page: Page):
    """
    Sets navigator.webdriver to false to avoid detection.
    """
    page.evaluate("Object.defineProperty(navigator, 'webdriver', { get: () => false })")


def visit_url_with_params(page: Page, url: str, params: dict):
    url = add_params_to_url(url, params)
    return page.goto(url)


def visit_google_cache(page: Page, url: str, params: dict = {}):
    """
    https://webcache.googleusercontent.com/search?q=cache:<url>
    If a webpage is too heavily protected and frequent updates are unnecessary,
    consider scraping google's cached version of the page instead.
    """
    CACHE_URL = "https://webcache.googleusercontent.com/search?q=cache"
    url = add_params_to_url(url, params)
    return page.goto(f"{CACHE_URL}:{url}")


def block_resources(
    page: Page,
    resources: list[str] = [
        "image",
        "stylesheet",
        "media",
        "font",
        "other",
    ],
):
    """
    To improve efficiency, exclude unnecessary elements from loading.
    See https://scrapingant.com/blog/block-requests-playwright
    """

    def route_guard(route: Route, request: Request):
        # Block requests for excluded resource types
        if request.resource_type in resources:
            route.abort()
        else:
            route.continue_()

    page.route("**/*", route_guard)


def wait_for_text(page: Page, selector: str):
    """
    Wait for element to have text.
    """
    page.wait_for_selector(selector)
    script = f"() => {{return document.querySelector('{selector}').innerText.trim();}}"
    return page.wait_for_function(script)


class QSyncPlaywright:
    def __init__(self):
        self._p = None
        self._initialized = False

        self.initialize()

    def initialize(self):
        if not self._initialized:
            self._p = sync_playwright().start()
            self._initialized = True

    def launch_browser(self, *args, **kwargs):
        return self._p.chromium.launch(*args, **kwargs)

    def launch_persistent_context(self, path: str, *args, **kwargs):
        """
        For launching a persistent browser from a given path.
        The path must lead to an existing folder.
        Once launched for the first time, the folder will populate with a session.
        """
        return self._p.chromium.launch_persistent_context(
            user_data_dir=path, *args, **kwargs
        )

    def close(self):
        if self._initialized:
            self._p.stop()
            self._initialized = False
            print("Playwright closed.")
