import json
import shutil
from operator import attrgetter, itemgetter, methodcaller
from pathlib import Path

import pytest

from scrapers.eu_trans import Scraper
from tests import SAMPLES

EU_TRANS_SAMPLES = SAMPLES / "eu_trans"

STORIES_URL = "https://europeana.transcribathon.eu/documents/?offset={}"
STORY_URL = "https://europeana.transcribathon.eu/documents/story/?story={}"
ITEM_URL = "https://europeana.transcribathon.eu/documents/story/item/?item={}"

HASH_PAGE_MAPPING = {
    # Search pages
    "c30c9f2dc5c05d5419425f26818c355a": "stories",
    "01d264398b6493b820cbefa8e0cb52eb": "no_stories",
    # Story 126760 with one item
    "013bcfada8fc924cfdd2e6df1e08a44e": "story_126760",
    "404c22ac8911abcdcefa077168ad4acb": "item_39133712",
    # Story 110349 with three items
    "2cb0125a9bf22cd9cc113cba1f118ff2": "story_110349",
    "d046ec31ac10265708165940465dd8f9": "item_1100686",
    "37f945d9bb24eae59e5629e8b3834727": "item_1100689",
    "61f8424086519f9ada0d1d85927a0446": "item_1100691",
}


def sort_json_content(content):
    def sort_metadata(value):
        return sorted(value, key=itemgetter("type", "name", "value"))

    content = json.loads(content)

    # When the HTML is parsed, order can change
    # So we update the `Agent *` metadata to allow comparison
    for i in range(len(content["metadata"])):
        if "Agent" not in content["metadata"][i]["name"]:
            continue
        content["metadata"][i]["name"] = "Agent"

    # Sort all list of dict to compare them
    content["metadata"] = sort_metadata(content["metadata"])
    for i in range(len(content["items"])):
        content["items"][i]["metadata"] = sort_metadata(content["items"][i]["metadata"])

    return content


@pytest.mark.parametrize(("cached_pages"), [True, False])
def test_euro_trans(cached_pages, requests_mock, tmp_path):
    output_dir = tmp_path / "data"

    if not cached_pages:
        # Search pages
        requests_mock.get(
            STORIES_URL.format(1),
            text=(EU_TRANS_SAMPLES / "stories.html").read_text(),
        )
        requests_mock.get(
            STORIES_URL.format(2),
            text=(EU_TRANS_SAMPLES / "no_stories.html").read_text(),
        )

        # Story 126760 with one item
        requests_mock.get(
            STORY_URL.format(126760),
            text=(EU_TRANS_SAMPLES / "story_126760.html").read_text(),
        )
        requests_mock.get(
            ITEM_URL.format(39133712),
            text=(EU_TRANS_SAMPLES / "item_39133712.html").read_text(),
        )

        # Story 110349 with three items
        requests_mock.get(
            STORY_URL.format(110349),
            text=(EU_TRANS_SAMPLES / "story_110349.html").read_text(),
        )
        requests_mock.get(
            ITEM_URL.format(1100686),
            text=(EU_TRANS_SAMPLES / "item_1100686.html").read_text(),
        )
        requests_mock.get(
            ITEM_URL.format(1100689),
            text=(EU_TRANS_SAMPLES / "item_1100689.html").read_text(),
        )
        requests_mock.get(
            ITEM_URL.format(1100691),
            text=(EU_TRANS_SAMPLES / "item_1100691.html").read_text(),
        )

        expected_requests = [
            # Search page
            "https://europeana.transcribathon.eu/documents/?entity=transcription&filter_query=%7B%22TranscriptionSource%22%3A%22manual%22%7D&offset=1",
            "https://europeana.transcribathon.eu/documents/?entity=transcription&filter_query=%7B%22TranscriptionSource%22%3A%22manual%22%7D&offset=2",
            # Story 126760 with one item
            "https://europeana.transcribathon.eu/documents/story/?story=126760",
            "https://europeana.transcribathon.eu/documents/story/item/?item=39133712",
            # Story 110349 with three items
            "https://europeana.transcribathon.eu/documents/story/?story=110349",
            "https://europeana.transcribathon.eu/documents/story/item/?item=1100686",
            "https://europeana.transcribathon.eu/documents/story/item/?item=1100689",
            "https://europeana.transcribathon.eu/documents/story/item/?item=1100691",
        ]
    else:
        # Populate cache
        (output_dir / "html").mkdir(parents=True)
        for file_hash, filename in HASH_PAGE_MAPPING.items():
            shutil.copy(
                (EU_TRANS_SAMPLES / filename).with_suffix(".html"),
                (output_dir / "html" / file_hash).with_suffix(".html"),
            )
        expected_requests = []

    Scraper(output_dir=output_dir).run()

    # Check files
    expected_paths = [
        # Extracted data
        output_dir / "110349.json",
        output_dir / "126760.json",
        # Cache files
        output_dir / "html" / "013bcfada8fc924cfdd2e6df1e08a44e.html",
        output_dir / "html" / "01d264398b6493b820cbefa8e0cb52eb.html",
        output_dir / "html" / "2cb0125a9bf22cd9cc113cba1f118ff2.html",
        output_dir / "html" / "37f945d9bb24eae59e5629e8b3834727.html",
        output_dir / "html" / "404c22ac8911abcdcefa077168ad4acb.html",
        output_dir / "html" / "61f8424086519f9ada0d1d85927a0446.html",
        output_dir / "html" / "c30c9f2dc5c05d5419425f26818c355a.html",
        output_dir / "html" / "d046ec31ac10265708165940465dd8f9.html",
    ]
    assert (
        sorted(list(filter(methodcaller("is_file"), output_dir.rglob("*"))))
        == expected_paths
    )

    for story_path in expected_paths:
        file_name = (
            Path(HASH_PAGE_MAPPING[story_path.stem]).with_suffix(".html")
            if story_path.suffix == ".html"
            else story_path.name
        )
        content, expected_content = (
            story_path.read_text(),
            (EU_TRANS_SAMPLES / file_name).read_text(),
        )
        # Allow to compare list of dict
        if story_path.suffix == ".json":
            content, expected_content = (
                sort_json_content(content),
                sort_json_content(expected_content),
            )

        assert content == expected_content

    # Check requests
    assert sorted(map(attrgetter("url"), requests_mock.request_history)) == sorted(
        expected_requests
    )
