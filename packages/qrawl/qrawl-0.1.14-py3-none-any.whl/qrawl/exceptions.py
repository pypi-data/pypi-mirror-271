from lytils import ctext


class FakeUserAgentNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>Module 'fake-useragent' not installed.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)
