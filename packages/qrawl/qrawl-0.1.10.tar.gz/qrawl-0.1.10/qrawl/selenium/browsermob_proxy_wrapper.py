# Standard Libraries
from base64 import b64decode
import json
import time

# Third-party Libraries
from lytils import cprint
from lytils.file import LyFile
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
    def __init__(self, browsermob_proxy_path: str, port=9090, debug: bool = False):
        self._debug = debug
        if Server is None:
            raise BrowsermobProxyNotInstalled
        if psutil is None:
            raise PsutilNotInstalled
        if not browsermob_proxy_path:
            raise MissingBrowsermobProxyPath

        options = {"port": port}

        if self._debug:
            cprint(f"<y>DEBUG: BMP browsermob_proxy_path = {browsermob_proxy_path}")
            cprint(f"<y>DEBUG: BMP port = {port}")
            options.update({"log_path": "browsermob-proxy.log"})

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

    def _get_response_from_content(self, content: dict, debug: bool = False):
        debug_path = "debug/BMP/_get_response_from_content.txt"

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

                if debug:
                    # Print request url and response
                    append_line(debug_path, decoded_str)

                return json.loads(decoded_str)

        except KeyError:
            # response -> content -> text does not exist
            raise KeyError

    def wait_for_response(
        self,
        partial_request_url: str,
        poll_interval: int = 1,
        timeout: int = 10,
        debug: bool = False,
    ):
        """
        Either returns a response or raises a timeout exception.
        """
        debug_file = LyFile("debug/BMP/wait_for_response.txt")
        if debug:
            debug_file.create()

        start_time = time.time()  # Record start time for timeout

        while time.time() - start_time < timeout:

            for entry in self._client.har["log"]["entries"]:

                if partial_request_url in json.dumps(entry["request"]["url"]):

                    if debug:
                        # Print request url and response
                        debug_file.append(entry["request"]["url"])
                        debug_file.append_json(entry["response"])

                    content = entry["response"]["content"]

                    try:
                        # No decoding necessary
                        return self._get_response_from_content(content, debug=True)

                    except KeyError:
                        # response -> content -> text does not exist
                        continue

            # ping requests against after interval has passed
            time.sleep(poll_interval)

        # If code reaches outside of loop, it is because of timeout.

        if debug:
            duration = time.time() - start_time
            debug_file.append(f"Timed out. Duration: {round(duration, 3)} seconds.")

        raise TimeoutException

    # Troubleshoot request urls
    def get_request_urls(self):
        request_urls = []
        for entry in self._client.har["log"]["entries"]:
            request_urls.append(entry["request"]["url"])
        return request_urls

    def get_responses(self, partial_request_url: str, debug: bool = False):
        debug_file = LyFile("debug/BMP/get_responses.txt")
        if debug:
            debug_file.create()

        responses = []
        for entry in self._client.har["log"]["entries"]:

            if partial_request_url in entry["request"]["url"]:

                if debug:
                    # Print request url and response
                    debug_file.append(entry["request"]["url"])
                    debug_file.append_json(entry["response"])

                content = entry["response"]["content"]

                try:
                    response = self._get_response_from_content(content, debug=False)
                    responses.append(response)

                except KeyError:
                    continue

        if debug and len(responses) == 0:
            debug_file.append(f"url '{partial_request_url}' not found.")

        return responses

    def close(self):
        self._client.close()
        self._server.stop()
