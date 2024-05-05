from lytils import ctext


# * MODULE NOT INSTALLED Exceptions
class BrowsermobProxyNotInstalled(Exception):
    # Raise this when browsermob proxy path is missing
    def __init__(
        self,
        message="Module 'browsermob-proxy' not installed.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class PsutilNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>Module 'psutil' not installed.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class SeleniumWireNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>Module 'selenium-wire' not installed or 'blinker@1.7.0' is not installed.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


class UndetectedChromedriverNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>Module 'undetected_chromedriver' not installed.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)


# * MISCELLANEOUS Exceptions
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
