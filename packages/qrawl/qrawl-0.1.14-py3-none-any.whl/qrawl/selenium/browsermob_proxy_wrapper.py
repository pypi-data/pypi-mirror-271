# Standard Libraries
from base64 import b64decode
import json
import time

# Third-party Libraries
from lytils.logger import LyLogger
from lytils.regex import match
from selenium.common.exceptions import TimeoutException

# * OPTIONAL IMPORTS
try:
    from browsermobproxy import Server
except ModuleNotFoundError:
    Server = None

try:
    import psutil  # type: ignore
except ModuleNotFoundError:
    psutil = None

# Local Libraries
from .exceptions import BrowsermobProxyNotInstalled
from .exceptions import MissingBrowsermobProxyPath
from .exceptions import PsutilNotInstalled


class BrowsermobProxyWrapper:
    def __init__(
        self,
        browsermob_proxy_path: str,
        port: int = 9090,
        log_path="logs/BMP",
        log_level="warning",
    ):
        """
        Wrapper for browsermob-proxy utility for Selenium.

        Args:
            browsermob_proxy_path (str): Path of browsermob proxy installation.
            port (int): Port to run browsermob proxy server on.
            log_path (str): Directory path to store browsermob proxy related logs.
            log_level (str): Level of logs desired. From least to most: debug > info > warning > error > critical.
        """

        if Server is None:
            raise BrowsermobProxyNotInstalled
        if psutil is None:
            raise PsutilNotInstalled
        if not browsermob_proxy_path:
            raise MissingBrowsermobProxyPath

        self.log_path = log_path
        self.log_level = log_level

        options = {"port": port}
        options.update({"log_path": f"{log_path}/browsermob-proxy.log"})

        self.kill_existing_bmp()  # Kill existing browsermob proxies before starting
        self._server = Server(browsermob_proxy_path, options=options)
        self._client = None

    def kill_existing_bmp(self):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == "browsermob-proxy":
                proc.kill()

    def start_server(self):
        self._server.start()
        return self._server

    def start_client(self):
        # Disable certificate checks. Proxy will trust all of the servers.
        # ! Only use "trustAllServers" with crawling/testing, unsafe to use for browsing.
        # params = { "trustAllServers": "true" }
        params = {}
        self._client = self._server.create_proxy(params=params)
        return self._client

    def server(self):
        return self._server

    def client(self):
        return self._client

    def proxy_url(self):
        return self._client.proxy

    def start_har(self, name: str | None = None):
        # Possible HAR options
        # Source: https://medium.com/@jiurdqe/how-to-get-json-response-body-with-selenium-amd-browsermob-proxy-71f10335c66
        options = {
            "captureHeaders": True,
            "captureContent": True,
            "captureBinaryContent": True,
        }
        self._client.new_har(name, options=options)

    def har(self):
        return self._client.har

    def _get_response_from_content(self, content: dict):
        logger = LyLogger(
            "bmp_get_response_from_content"
            f"{self.log_path}/_get_response_from_content.log",
            level=self.log_level,
        )

        try:
            # No decoding necessary
            return json.loads(content["text"])

        except json.decoder.JSONDecodeError:
            # response -> content -> text is not a json string
            encoding = content["encoding"]

            if encoding == "base64":
                charset = match(r"(?<=charset=).+", content["mimeType"])
                decoded_bytes = b64decode(content["text"])

                # decoded_str = decoded_bytes.decode(charset)
                decoded_str = decoded_bytes.decode(charset)

                logger.debug(decoded_str)

                return json.loads(decoded_str)

        except KeyError:
            # response -> content -> text does not exist
            raise KeyError

    def wait_for_response(
        self,
        partial_request_url: str,
        poll_interval: int = 1,
        timeout: int = 10,
    ):
        """
        Either returns a response or raises a timeout exception.
        """
        logger = LyLogger(
            "bmp_wait_for_response" f"{self.log_path}/_wait_for_response.log",
            level=self.log_level,
        )

        start_time = time.time()  # Record start time for timeout

        while time.time() - start_time < timeout:

            for entry in self._client.har["log"]["entries"]:

                if partial_request_url in json.dumps(entry["request"]["url"]):

                    # Print request url and response
                    logger.debug_json(
                        f'BMP: {entry["request"]["url"]}:',
                        entry["response"],
                    )

                    content = entry["response"]["content"]

                    try:
                        # No decoding necessary
                        return self._get_response_from_content(content)

                    except KeyError:
                        # response -> content -> text does not exist
                        continue

            # ping requests against after interval has passed
            time.sleep(poll_interval)

        # If code reaches outside of loop, it is because of timeout.

        duration = time.time() - start_time
        logger.info(f"Timed out. Duration: {round(duration, 3)} seconds.")

        raise TimeoutException

    # Troubleshoot request urls
    def get_request_urls(self):
        request_urls = []
        for entry in self._client.har["log"]["entries"]:
            request_urls.append(entry["request"]["url"])
        return request_urls

    def get_responses(self, partial_request_url: str):
        logger = LyLogger(
            "bmp_get_responses" f"{self.log_path}/get_responses.log",
            level=self.log_level,
        )

        responses = []
        for entry in self._client.har["log"]["entries"]:

            if partial_request_url in entry["request"]["url"]:

                # Print request url and response
                logger.debug_json(
                    f'BMP: {entry["request"]["url"]}:',
                    entry["response"],
                )

                content = entry["response"]["content"]

                try:
                    response = self._get_response_from_content(content)
                    responses.append(response)

                except KeyError:
                    continue

        if len(responses) == 0:
            logger.info(f"Url '{partial_request_url}' not found.")

        return responses

    def close(self):
        self._client.close()
        self._server.stop()
