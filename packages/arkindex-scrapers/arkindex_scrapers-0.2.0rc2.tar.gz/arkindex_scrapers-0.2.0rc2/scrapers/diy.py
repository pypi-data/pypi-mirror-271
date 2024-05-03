import json
import logging
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import requests
import tqdm
from bs4 import BeautifulSoup

from scrapers.utils import BaseObject
from scrapers.utils import Item as BaseItem
from scrapers.utils import Scraper as BaseScraper

logger = logging.getLogger(__name__)

COLLECTION_URL_PATH = "/collections/show/{}/"
ITEM_URL_PATH = "/items/show/{}/"
TRANSCRIBE_URL_PATH = "/transcribe/{}/{}/"


@dataclass
class Item(BaseObject):
    def build_name(self) -> str:
        collection_title = self.page.find("h1", class_="header collection-title")
        if collection_title:
            return collection_title.text

        logger.warning(f"Name not found for item {self.id}")
        return super().build_name()


@dataclass
class ChildItem(BaseItem):
    image_path: str | None = ""

    output_dir: Path | None = None

    def __post_init__(self, id: str, url: str, page: BeautifulSoup) -> None:
        super().__post_init__(id, url, page)

        self.image_path = self.build_image_path()

    @staticmethod
    def dict_factory(fields):
        # Do not export these parameters when converting in dict
        excluded_fields = ("output_dir",)
        return {key: value for key, value in fields if key not in excluded_fields}

    def build_name(self) -> str:
        titles = self.page.find_all("p", class_="titles")
        for title in titles:
            # This is not the title of a parent
            if not title.find("a"):
                return title.text

        logger.warning(f"Name not found for item {self.id}")
        return super().build_name()

    def build_transcriptions(self) -> list[str]:
        transcribebox = self.page.find("textarea", id="transcribebox")

        if not transcribebox:
            logger.warning(f"Transcription not found for item {self.id}")
            return ""

        return [*super().build_transcriptions(), transcribebox.text.strip()]

    def build_image_path(self) -> str:
        # Image is required, raise error if we don't find it
        assert self.output_dir.is_dir(), f"{self.output_dir} is not a valid directory"

        image = self.page.find("img", id="ImageID")
        assert image, "Image not found"

        image_url = image.get("src")
        assert image_url, "Image has no source"

        image_name = image_url.split("/")[-1]
        image_path = (self.output_dir / image_name).with_suffix(Path(image_url).suffix)
        if not image_path.exists():
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image_path.write_bytes(response.content)

        return image_name


class Scraper(BaseScraper):
    def __init__(
        self,
        collection_id: int,
        output_dir: Path,
        base_url: str = "http://s-lib017.lib.uiowa.edu",
    ):
        self.collection_id = collection_id

        super().__init__(output_dir, base_url)

    def run(self):
        collection_soup, _ = self.get_html(
            COLLECTION_URL_PATH.format(self.collection_id)
        )
        logger.info(f"Retrieving collection {self.collection_id}…")

        for item in tqdm.tqdm(
            collection_soup.find_all(class_="col-xs-1 collection-item")
        ):
            item_links = list(
                set(
                    [
                        a_link["href"]
                        for a_link in item.find_all(href=re.compile("items"))
                    ]
                )
            )
            for link_part in item_links:
                item_id = link_part.split("/")[-1]
                item_soup, item_link = self.get_html(ITEM_URL_PATH.format(item_id))
                item_dict = {
                    **asdict(
                        Item(
                            id=item_id,
                            url=item_link,
                            page=item_soup,
                        )
                    ),
                    "items": [],
                }
                logger.info(
                    f"Getting images and transcriptions from item {item_dict['name']}…"
                )
                child_items = item_soup.find_all(class_="col-xs-1 item-item")
                logger.info(f"{len(child_items)} images to download.")
                for child_item in tqdm.tqdm(child_items):
                    child_item_links = list(
                        set(
                            [
                                a_link["href"]
                                for a_link in child_item.find_all(
                                    href=re.compile("transcribe")
                                )
                            ]
                        )
                    )
                    for child_item_link in child_item_links:
                        child_item_id = child_item_link.split("/")[-1]
                        child_item_soup, child_item_link = self.get_html(
                            TRANSCRIBE_URL_PATH.format(item_id, child_item_id)
                        )
                        item_dict["items"].append(
                            asdict(
                                ChildItem(
                                    id=child_item_id,
                                    url=child_item_link,
                                    page=child_item_soup,
                                    output_dir=self.output_dir,
                                ),
                                dict_factory=ChildItem.dict_factory,
                            )
                        )

                # Save in a JSON file
                item_path = (self.output_dir / item_id).with_suffix(".json")
                item_path.write_text(json.dumps(item_dict, indent=4))


def run(*args, **kwargs):
    Scraper(*args, **kwargs).run()
