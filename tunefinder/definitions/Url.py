from urllib.parse import urlparse


class Url:
    def __init__(self, url: str):
        self.str = url

        parsed_url = urlparse(url)
        self.scheme = parsed_url.scheme
        self.hostname = parsed_url.netloc
        self.path = parsed_url.path
