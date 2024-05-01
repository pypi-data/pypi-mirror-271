# Standard Libraries
import json
import os
from urllib.parse import urlencode

# Third-Party Libraries
# * OPTIONAL Imports
try:
    from fake_useragent import FakeUserAgent
except ModuleNotFoundError:
    FakeUserAgent = None

# Local libraries
from .exceptions import FakeUserAgentNotInstalled


def add_params_to_url(url: str, params: dict) -> str:
    return f"{url}?{urlencode(params)}"


def get_cookie_header(cookies: list[dict]):
    return "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])


def get_random_user_agent() -> str:
    if FakeUserAgent is None:
        raise FakeUserAgentNotInstalled
    ua = FakeUserAgent()
    return ua.random


def get_schema_from_json(data: dict, output: str = "schema.json", sample_size: int = 3):
    """
    Outputs schema of the data given a json object.
    @output: file to output schema to
    @sample_size: number of data samples
    """
    directory = os.path.dirname(output)

    if "/" in output and not os.path.exists(directory):
        # Create the directory if it DOESN'T exist
        os.makedirs(directory)

    with open(output, "w") as f:
        sample = data[:sample_size]
        json.dump(sample, f, indent=4)
        f.close()
