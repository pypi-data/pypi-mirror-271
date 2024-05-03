import logging
from dataclasses import InitVar, dataclass, field
from functools import cached_property
from hashlib import md5
from pathlib import Path
from urllib.parse import ParseResult

import requests
from apistar.exceptions import ErrorResponse
from bs4 import BeautifulSoup
from requests.compat import urlencode, urljoin, urlparse
from requests.exceptions import HTTPError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from arkindex import ArkindexClient

logger = logging.getLogger(__name__)


def _is_500_error(exc: Exception) -> bool:
    """
    Check if an API error has a HTTP 5xx error code.
    Used to retry most API calls in [Scraper][scrapers.utils.Scraper].
    :param exc: Exception to check
    """
    if not isinstance(exc, HTTPError) or not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.response.status_code < 600


@dataclass
class BaseObject:
    id: InitVar[str]
    url: InitVar[str]

    page: InitVar[BeautifulSoup]

    name: str | None = ""
    metadata: list[dict] | None = field(default_factory=list)

    def __post_init__(self, id: str, url: str, page: BeautifulSoup) -> None:
        self.id = id
        self.url = url
        self.page = page

        self.name = self.build_name()
        self.metadata = self.build_metadata()

    def build_name(self) -> str:
        return self.id

    def build_metadata(self) -> list[dict]:
        return [
            {
                "type": "reference",
                "name": "ID",
                "value": self.id,
            },
            {
                "type": "url",
                "name": "URL",
                "value": self.url,
            },
        ]


@dataclass
class Item(BaseObject):
    transcriptions: list[str] = field(default_factory=list)

    def __post_init__(self, id: str, url: str, page: BeautifulSoup) -> None:
        super().__post_init__(id, url, page)

        self.transcriptions = self.build_transcriptions()

    def build_transcriptions(self) -> list[str]:
        return []


class Scraper:
    def __init__(self, output_dir: Path, base_url: str):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.html_cache_dir = self.output_dir / "html"
        self.html_cache_dir.mkdir(exist_ok=True)

        self.base_url = base_url

    @cached_property
    def base_url_parsed(self) -> ParseResult:
        return urlparse(self.base_url)

    @retry(
        retry=retry_if_exception(_is_500_error),
        wait=wait_exponential(multiplier=2, min=3),
        reraise=True,
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def get_html(
        self, path: str, params: dict | None = None
    ) -> tuple[BeautifulSoup, str]:
        if params is None:
            params = {}
        url = urljoin(self.base_url, path)
        if params:
            url += "?" + urlencode(params, True)

        # Check if we already have this page in cache
        url_hash = md5(url.encode("utf-8")).hexdigest()
        html_file = (self.html_cache_dir / url_hash).with_suffix(".html")
        if html_file.is_file():
            return BeautifulSoup(html_file.read_text(), "html.parser"), url

        response = requests.get(url)
        response.raise_for_status()

        # Cache this page
        page = response.text
        html_file.write_text(page)

        # Return the response.url to store it as metadata
        return BeautifulSoup(page, "html.parser"), response.url


class ArkindexAPIClient(ArkindexClient):
    @retry(
        reraise=True,
        retry=retry_if_exception(_is_500_error),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def request(self, operation_id, *args, **kwargs):
        return super().request(operation_id, *args, **kwargs)


def hash_image(path: Path) -> str:
    md5_hasher = md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hasher.update(chunk)

    return md5_hasher.hexdigest()
