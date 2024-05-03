import json
import logging
import re
from collections.abc import MutableSet
from dataclasses import asdict, dataclass
from datetime import datetime
from functools import cached_property
from operator import attrgetter
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag
from dateutil import parser
from dateutil.parser import ParserError
from requests.compat import urlparse, urlunparse

from scrapers.utils import BaseObject as BaseBaseObject
from scrapers.utils import Item as BaseItem
from scrapers.utils import Scraper as BaseScraper
from teklia_toolbox.time import Timer

logger = logging.getLogger(__name__)

STORIES_URL_PATH = "/documents/"
STORY_URL_PATH = "/documents/story/"
ITEM_URL_PATH = "/documents/story/item/"

STORY_PARAM_PATTERN = re.compile(r"story=(\d+)")
ITEM_PARAM_PATTERN = re.compile(r"item=(\d+)")

IIIF_PATH_PATTERN = re.compile(r"/full/full/0/.*")
SEVERAL_SLASHES_PATTERN = re.compile(r"\/+")

DATE_METADATA = ["Date", "Begin", "End", "Created"]


@dataclass
class BaseObject(BaseBaseObject):
    def get_metadata(self) -> MutableSet[tuple[str, str]]:
        return set()

    def build_metadata(self) -> list[dict]:
        def clean_metadata_name(name):
            return name.replace("Document", "").strip()

        def metadata_type(name, value):
            name = clean_metadata_name(name)
            if name in DATE_METADATA:
                return "date"
            if value.startswith("http") and " " not in value.strip():
                return "url"
            return "reference"

        extra_metadata = []

        metadata = self.get_metadata()
        if metadata:
            extra_metadata.extend(
                [
                    {
                        "type": metadata_type(name, value),
                        "name": clean_metadata_name(name),
                        "value": value.strip(),
                    }
                    for (name, value) in metadata
                    if clean_metadata_name(name) and value.strip()
                ]
            )
        else:
            logger.warning(
                f"Metadata not found for {self.__class__.__name__.lower()} {self.id}"
            )

        return super().build_metadata() + extra_metadata


@dataclass
class Item(BaseObject, BaseItem):
    iiif_url: str | None = ""

    def __post_init__(self, id: str, url: str, page: BeautifulSoup) -> None:
        super().__post_init__(id, url, page)

        self.iiif_url = self.build_iiif_url()

    @cached_property
    def transcription_container(self) -> Tag | None:
        return self.page.find("div", id="transcription-container")

    def get_dates(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id='description-editor'>
                ...
                <div class='document-date-container'>
                    <div class='date-top'>
                        <!-- Meta title -->
                        <div>Start Date:</div>
                        <!-- Meta title -->
                        <div>End Date:</div>
                    </div>
                    ...
                    <div class='date-bottom'>
                        <!-- Meta value -->
                        <div>05/06/1915</div>
                        <!-- Meta value -->
                        <div></div>
                    </div>
                </div>
            </div>
        ```
        """
        # Extract `Date`
        description_editor = self.page.find("div", id="description-editor")
        if not description_editor:
            return set()

        document_date_container = description_editor.find(
            "div", class_="document-date-container"
        )
        if not document_date_container:
            return set()

        return {
            (meta_title.text.replace(":", ""), value.text)
            for meta_title, value in zip(
                document_date_container.find("div", class_="date-top"),
                document_date_container.find("div", class_="date-bottom"),
                strict=False,
            )
        }

    def get_keywords(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id="item-page-keyword-container">
                <div>
                    <!-- Meta title -->
                    <h6>Keywords</h6>
                </div>
                ...
                <div>
                    <!-- Meta value -->
                    <div class="keyword-single">French</div>
                    <!-- Meta value -->
                    <div class="keyword-single">English</div>
                </div>
            </div>
        ```
        """
        # Extract `Type` & `Keywords`
        keywords = set()
        for keywords_tag_id in ["doc-type-area", "item-page-keyword-container"]:
            keywords_tag = self.page.find("div", id=keywords_tag_id)
            if not keywords_tag:
                continue

            meta_title = keywords_tag.find("h6")
            if not meta_title:
                continue

            keywords.update(
                {
                    (meta_title.text, keyword_single.text)
                    for keyword_single in keywords_tag.find_all(
                        "div", class_="keyword-single"
                    )
                }
            )

        return keywords

    def get_description(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id="description-area">
                <!-- Meta title -->
                <h6>Description</h6>
                ...
                <!-- Meta value -->
                <div class="current-description">
                    wydruk z amerykańskiego tygodnika społeczno-politycznego "Time"
                </div>

                <div class="description-language">
                    <!-- Meta title -->
                    <h6> Language of Description </h6>
                    <div>
                        <!-- Meta value -->
                        <div class="language-single">Polski</div>
                    </div>
                </div>
            </div>
        ```
        """
        # Extract `Description`
        description_area = self.page.find("div", id="description-area")
        if not description_area:
            return set()

        meta_title = description_area.find("h6")
        current_description = description_area.find("div", class_="current-description")
        if not meta_title or not current_description:
            return set()

        description = {(meta_title.text, current_description.text)}

        # Extract `Language of Description`
        description_language = description_area.find(
            "div", class_="description-language"
        )
        if not description_language:
            return description

        meta_title = description_language.find("h6")
        if not meta_title:
            return description

        description.update(
            {
                (meta_title.text, language_single.text)
                for language_single in description_language.find_all(
                    "div", class_="language-single"
                )
            }
        )

        return description

    def get_external_web_resources(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id="item-page-link-container">
                <div>
                    <!-- Meta title -->
                    <h6>External Web Resources</h6>
                </div>
                ...
                <div>
                    ...
                    <div>
                        ...
                        <!-- Meta value -->
                        <a href="https://www.cwgc.org/visit-us/find-cemeteries-memorials/cemetery-details/80800/thiepval-memorial/" target="_blank">https://www.cwgc.org/visit-us/find-cemeteries-memorials/cemetery-details/80800/thiepval-memorial/</a>
                    </div>
                    <div>
                        ...
                        <!-- Meta value -->
                        <a href="https://www.cwgc.org/find-records/find-war-dead/casualty-details/608894/james-healy/" target="_blank">https://www.cwgc.org/find-records/find-war-dead/casualty-details/608894/james-healy/</a>
                    </div>
                </div>
            </div>
        ```
        """
        # Extract `External Web Resources`
        item_page_link_container = self.page.find("div", id="item-page-link-container")
        if not item_page_link_container:
            return set()

        meta_title = item_page_link_container.find("h6")
        if not meta_title:
            return set()

        return {
            (meta_title.text, link.attrs.get("href"))
            for link in item_page_link_container.find_all("a")
        }

    def get_people(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id="tagging-section">
                <div>
                    <!-- Meta title -->
                    <h6>People</h6>
                </div>
                ...
                <div>
                    ...
                    <!-- Meta value -->
                    <div class="single-person">
                        <p><span>Charles  Dangeuger</span> (Birth: 27/03/1888, Juziers (Yvelines) - Death: 22/08/1914, Neufchateau)</p>
                        <p>Description: KIA, 2nd class, 23rd Colonial Infantry Regiment</p>
                    </div>
                </div>
            </div>
        ```
        """
        # Extract `People`
        tagging_section = self.page.find("div", id="tagging-section")
        if not tagging_section:
            return set()

        meta_title = tagging_section.find("h6")
        if not meta_title:
            return set()

        return {
            (meta_title.text, single_person.get_text(separator="\n", strip=True))
            for single_person in tagging_section.find_all("div", class_="single-person")
        }

    def get_location(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id="location-editor">
                ...
                <div>
                    ...
                    <div>
                        <!-- Meta value -->
                        <p><b>International Red Cross</b> (46.2018, 6.1466)</p>
                        <!-- Do not export this description -->
                        <p>Wikidata Reference: <b><a href="http://wikidata.org/wiki/Q71">Geneva, Q71</a></b></p>
                    </div>
                </div>
            </div>
        ```
        """
        # Extract `Location`
        location_editor = self.page.find("div", id="location-editor")
        if not location_editor:
            return set()

        return {
            (
                "Location",
                location_single.find("p").get_text(separator=" ", strip=True),
            )
            for location_single in location_editor.children
            if location_single.find("p")
        }

    def get_metadata(self) -> MutableSet[tuple[str, str]]:
        # Each metadata has its own tree/tag...
        return {
            *self.get_dates(),
            *self.get_keywords(),
            *self.get_description(),
            *self.get_external_web_resources(),
            *self.get_people(),
            *self.get_location(),
        }

    def get_languages(self) -> list[str]:
        if not self.transcription_container:
            return []

        transcription_language = self.transcription_container.find(
            "div", class_="transcription-language"
        )
        if not transcription_language:
            return []

        return list(
            filter(
                lambda language: language,
                map(
                    attrgetter("text"),
                    transcription_language.find_all("div", class_="language-single"),
                ),
            )
        )

    def get_transcription_status(self) -> str:
        if not self.transcription_container:
            return ""

        status_display = self.transcription_container.find(
            "div", class_="status-display"
        )
        if not status_display:
            return ""

        return status_display.text

    def build_metadata(self) -> list[dict]:
        extra_metadata = []

        # Retrieve language
        languages = self.get_languages()
        if languages:
            extra_metadata.extend(
                [
                    {
                        "type": "reference",
                        "name": "Language",
                        "value": language,
                    }
                    for language in languages
                ]
            )
        else:
            logger.warning(f"Language(s) not found for item {self.id}")

        # Retrieve transcription status
        transcription_status = self.get_transcription_status()
        if transcription_status:
            extra_metadata.append(
                {
                    "type": "reference",
                    "name": "Transcription status",
                    "value": transcription_status,
                }
            )
        else:
            logger.warning(f"Transcription status not found for item {self.id}")

        return super().build_metadata() + extra_metadata

    def build_iiif_url(self) -> str:
        # IIIF URL is required, raise error if we don't find it
        input = self.page.find("input", id="image-data-holder")
        assert input, "Image data not found"

        value = input.attrs.get("value")
        assert value, "Image data has no value"

        iiif_url = json.loads(value).get("@id")
        assert iiif_url, "IIIF URL not found"

        # Build valid URL
        parsed_iiif_url = urlparse(iiif_url)

        # Add default scheme
        if not parsed_iiif_url.scheme:
            parsed_iiif_url = parsed_iiif_url._replace(scheme="https")
            parsed_iiif_url = urlparse(parsed_iiif_url.geturl())

        url = urlunparse(
            (
                parsed_iiif_url.scheme,
                IIIF_PATH_PATTERN.sub("", parsed_iiif_url.netloc),
                IIIF_PATH_PATTERN.sub("", parsed_iiif_url.path),
                parsed_iiif_url.params,
                IIIF_PATH_PATTERN.sub("", parsed_iiif_url.query),
                parsed_iiif_url.fragment,
            )
        )

        # Remove duplicate slashes except for the scheme (first occurrence)
        return SEVERAL_SLASHES_PATTERN.sub("/", url).replace("/", "//", 1)

    def build_transcriptions(self) -> list[str]:
        if not self.transcription_container:
            return []

        current_transcription = self.transcription_container.find(
            "div", class_="current-transcription"
        )
        if not current_transcription:
            logger.warning(f"Transcription not found for item {self.id}")
            return []

        # Remove text that is not part of the transcription but adds context
        for span_class in [
            # Uncertain text
            "tct-uncertain",
            # Information text
            "pos-in-text",
        ]:
            for span_tag in current_transcription.find_all("span", class_=span_class):
                span_tag.replaceWith("")

        return [current_transcription.get_text(separator="\n", strip=True)]


@dataclass
class Story(BaseObject):
    def get_name(self) -> str:
        story_title = self.page.find("h2", id="story-title")
        if not story_title:
            return ""

        return story_title.text

    def get_description(self) -> str:
        desc_paragraph = self.page.find("p", id="desc-paragraph")
        if not desc_paragraph:
            return ""

        return desc_paragraph.get_text(separator="\n", strip=True)

    def get_metadata(self) -> MutableSet[tuple[str, str]]:
        """
        The HTML should have a structure like:
        ```html
            <div id="metadata-container">
                <div class="meta-single">
                    <!-- Meta title -->
                    <p>Source</p>
                    <p>
                        <!-- Meta value -->
                        UGC
                        <br />
                    </p>
                </div>
                ...
                <div class="meta-single">
                    <!-- Meta title -->
                    <p>Rights</p>
                    <p>
                        <!-- Meta value -->
                        <a href="http://creativecommons.org/publicdomain/zero/1.0/">http://creativecommons.org/publicdomain/zero/1.0/</a>
                        <br />
                        <!-- Meta value -->
                        <a href="http://creativecommons.org/licenses/by-sa/3.0/">http://creativecommons.org/licenses/by-sa/3.0/</a>
                        <br />
                    </p>
                </div>
            </div>
        ```
        """
        metadata_container = self.page.find("div", id="metadata-container")
        if not metadata_container:
            return set()

        metadata = set()
        for meta_single in metadata_container.find_all("div", class_="meta-single"):
            meta_title = next(meta_single.children)
            if not meta_title or not meta_title.next_sibling:
                continue

            metadata.update(
                {
                    (meta_title.text, value)
                    for value in meta_title.next_sibling.get_text(
                        separator="\n", strip=True
                    ).split("\n")
                }
            )

        # Special case for `Agent` metadata which have this format:
        # Mr Cacheux | europeana19141918:agent/b355a9d4605116a9b5c74fac5e80da1f
        count = 0
        for meta_title, meta_value in metadata.copy():
            meta_values = meta_value.split("|")
            if meta_title != "Agent" or len(meta_values) != 2:
                continue

            count += 1
            meta_name, meta_id = meta_values

            metadata.remove((meta_title, meta_value))
            metadata.update(
                {
                    (f"{meta_title}Name {count}", meta_name),
                    (f"{meta_title}ID {count}", meta_id),
                }
            )

        # Special case for `Created` metadata which can have a lot of values.
        # Simplify them by removing time information, then duplicated metadata will be removed
        for meta_title, meta_value in metadata.copy():
            if meta_title != "Created":
                continue

            try:
                created_date = parser.parse(meta_value)
            except ParserError:
                logger.warning(
                    f"Failed to parse `Created` date {meta_value} for story {self.id}"
                )
                continue

            metadata.remove((meta_title, meta_value))
            metadata.add(
                (
                    meta_title,
                    str(
                        datetime(
                            year=created_date.year,
                            month=created_date.month,
                            day=created_date.day,
                            tzinfo=created_date.tzinfo,
                            fold=created_date.fold,
                        ).date()
                    ),
                )
            )

        return metadata

    def build_name(self) -> str:
        name = self.get_name()

        if not name:
            logger.warning(f"Name not found for story {self.id}")
            return super().build_name()

        return name

    def build_metadata(self) -> list[dict]:
        extra_metadata = []

        # Retrieve description
        description = self.get_description()
        if description:
            extra_metadata.append(
                {
                    "type": "text",
                    "name": "Description",
                    "value": description,
                }
            )
        else:
            logger.warning(f"Description not found for story {self.id}")

        return super().build_metadata() + extra_metadata


class Scraper(BaseScraper):
    def __init__(
        self,
        output_dir: Path,
        story_id: str | None = None,
        base_url: str = "https://europeana.transcribathon.eu",
    ):
        super().__init__(output_dir, base_url)
        self.story_id = story_id

    def extract_item(self, item_id: int) -> dict:
        logger.info(f"Extracting item {item_id}")
        item_page, item_url = self.get_html(ITEM_URL_PATH, params={"item": item_id})
        return asdict(
            Item(
                id=str(item_id),
                url=item_url,
                page=item_page,
            )
        )

    def extract_items(self, story_page: str):
        # Extract item IDs from the story page
        item_ids = story_page.find("div", id="item-ids")
        assert item_ids, "Item IDs not found"

        try:
            item_ids = json.loads(item_ids.text)
        except Exception:
            raise ValueError("Item IDs are invalid.")
        return list(map(self.extract_item, item_ids))

    def extract_id(self, link: Tag, path: str, pattern: re.Pattern) -> str | None:
        # Extracts ID from the URL if it is correct
        href = link.attrs.get("href")
        if not href:
            return

        # The URL is not from the same domain or has the wrong path
        url_parsed = urlparse(href)
        if (
            self.base_url_parsed.scheme != url_parsed.scheme
            or self.base_url_parsed.netloc != url_parsed.netloc
            or url_parsed.path != path
        ):
            return

        # The ID is not in the URL
        match = pattern.match(url_parsed.query)
        if not match:
            return

        return match.group(1)

    def extract_story_id(self, story_link: Tag) -> tuple[str | None, str | None]:
        return self.extract_id(story_link, STORY_URL_PATH, STORY_PARAM_PATTERN)

    def extract_story(self, story_id: str) -> None:
        logger.info(f"Extracting story {story_id}")

        # Check if file already exists
        story_path = (self.output_dir / story_id).with_suffix(".json")
        if story_path.is_file():
            logger.debug(f"Story {story_id} already extracted")
            return

        # Extract the story
        try:
            story_page, story_url = self.get_html(
                STORY_URL_PATH, params={"story": story_id}
            )
            story_json = {
                **asdict(
                    Story(
                        id=story_id,
                        url=story_url,
                        page=story_page,
                    )
                ),
                "items": self.extract_items(story_page),
            }
        except Exception as e:
            logger.error(f"Failed to extract story {story_id}: {e}")
            return

        # Save in a JSON file
        story_path.write_text(json.dumps(story_json, indent=4))

    def extract_page(self, offset: int) -> bool:
        page, _ = self.get_html(
            STORIES_URL_PATH,
            params={
                "entity": ["transcription"],
                "filter_query": '{"TranscriptionSource":"manual"}',
                "offset": offset,
            },
        )

        story_ids = set(
            map(self.extract_story_id, page.find_all("a", title="Story")),
        )
        # There are no more results, the maximum offset has been exceeded
        if not story_ids:
            return False

        logger.info(f"Extracting page n°{offset}")
        for story_id in story_ids:
            with Timer() as t:
                self.extract_story(story_id)
            logger.info(f"Story {story_id} extracted in {t.delta} second(s)")

        return True

    def run(self) -> None:
        # Extract a single story
        if self.story_id is not None:
            with Timer() as t:
                self.extract_story(self.story_id)
            logger.info(f"Story {self.story_id} extracted in {t.delta} second(s)")

        # Extract all stories
        else:
            offset = 1

            # Extract pages as long as there are results
            while self.extract_page(offset):
                offset += 1


def run(*args, **kwargs):
    Scraper(*args, **kwargs).run()
