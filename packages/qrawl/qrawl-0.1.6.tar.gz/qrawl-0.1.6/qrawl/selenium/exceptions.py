from lytils import ctext


# BMP Exceptions
class BrowsermobProxyNotInstalled(Exception):
    # Raise this when browsermob proxy path is missing
    def __init__(
        self,
        message="<y>'browsermob-proxy' is not installed. Run 'pip install browsermob-proxy'.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class MissingBrowsermobProxyPath(Exception):
    # Raise this when browsermob proxy path is missing
    def __init__(
        self,
        message="<y>'browsermob_proxy_path' is empty. Check your proxy configuration.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class SeleniumWireAndUndetectedChromedriverIncompatible(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>Selenium Wire and Undetected Chromedriver are incompatible. Please only set 'use_selenium_wire' OR 'use_undetected_chromedriver'.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class SeleniumWireNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>'seleniumwire' is not installed. Run 'pip install seleniumwire'.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class UndetectedChromedriverNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>'undetected_chromedriver' is not installed. Run 'pip install undetected_chromedriver'.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)
