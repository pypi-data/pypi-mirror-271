from typing import Callable

# Third-party libraries
from gspread_formatting import CellFormat
from lytils import cprint
from lytils.regex import match
from lytils.google_sheets import Column as GSColumn
from lytils.google_sheets.format import DefaultFormat


# GSColumn is a class used to configure GoogleSheet columns
# This Column class extends GSColumn to support columns for crawling
class Column(GSColumn):
    def __init__(
        self,
        header: str,
        xpath: str = "",
        regex: str | list[str] = "",
        transform: Callable[[str], str] | None = None,
        format: CellFormat = DefaultFormat(),
        width: int = 100,
    ):
        # Initialize GoogleSheet Column instance
        super().__init__(header=header, format=format, width=width)

        # Xpath used to locate element on webpage
        self._xpath = xpath

        # Allow for single regex or list of regex
        self._regex = regex

        # Last line of defense for manipulating the crawled data
        #   is calling a function to do so
        # Locating by xpath and applying regex should be more
        #   than enough for most scenarios
        self._transform = transform

    def has_xpath(self):
        return self._xpath != ""

    def get_xpath(self):
        return self._xpath

    def has_regex(self):
        return self._regex != ""

    def apply_regex(self, text: str) -> str:
        new_text = text
        if isinstance(self._regex, str):
            try:
                new_text = match(self._regex, new_text)
            except:
                cprint(f"<y>RegEx Error ::: regex: {self._regex}, text: {text}")
        else:
            for r in self._regex:
                try:
                    new_text = match(r, new_text)
                except:
                    cprint(f"<y>RegEx Error ::: regex: {r}, text: {text}")
                    break
        return new_text

    def has_transform(self):
        return self._transform != None

    # Takes a string and calls the transform function, returning
    # the transformed string
    def transform(self, text: str) -> str:
        return self._transform(text)
