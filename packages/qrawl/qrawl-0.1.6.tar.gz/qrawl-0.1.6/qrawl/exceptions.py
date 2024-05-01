from lytils import ctext


class FakeUserAgentNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>'fake-useragent' is not installed. Run 'pip install fake-useragent'.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)
