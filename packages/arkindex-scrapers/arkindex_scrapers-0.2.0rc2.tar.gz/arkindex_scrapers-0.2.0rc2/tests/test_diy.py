import shutil
from operator import attrgetter, methodcaller
from pathlib import Path

import pytest

from scrapers.diy import Scraper
from tests import SAMPLES

DIY_SAMPLES = SAMPLES / "diy"

COLLECTION_URL = "http://s-lib017.lib.uiowa.edu/collections/show/{}/"
ITEM_URL = "http://s-lib017.lib.uiowa.edu/items/show/{}/"
TRANSCRIBE_URL = "http://s-lib017.lib.uiowa.edu/transcribe/{}/{}/"
IMAGE_URL = "http://s-lib017.lib.uiowa.edu/files/original/{}"

HASH_PAGE_MAPPING = {
    # Collection page
    "6948ea08304931a3a46fe5c436270e8e": "collection_13",
    # Item 3197 with three transcribes
    "3759ad9c608ea220ebfc310a3017e511": "item_3197",
    "ba89de5fb79670953c5a0d2f857ced6f": "transcribe_77731",
    "e93c0fcc8d91f2a9bb66006254925c07": "transcribe_77744",
    "5e308a96a027959822177632f121383c": "transcribe_77746",
    # Item 3373 with two transcribes
    "2c87b9cc8e044a3c8b4170015b2da6aa": "item_3373",
    "ce0165e8f4d9e56df394c51b45423071": "transcribe_83670",
    "73bc940f8a4d4c69125f70f4036fe955": "transcribe_83671",
}


@pytest.mark.parametrize(("cached_pages"), [True, False])
def test_diy(cached_pages, requests_mock, tmp_path):
    output_dir = tmp_path / "data"

    if not cached_pages:
        # Collection page
        requests_mock.get(
            COLLECTION_URL.format(13),
            text=(DIY_SAMPLES / "collection_13.html").read_text(),
        )

        # Item 3197 with three transcribes
        requests_mock.get(
            ITEM_URL.format(3197),
            text=(DIY_SAMPLES / "item_3197.html").read_text(),
        )
        requests_mock.get(
            TRANSCRIBE_URL.format(3197, 77731),
            text=(DIY_SAMPLES / "transcribe_77731.html").read_text(),
        )
        requests_mock.get(
            IMAGE_URL.format("9d5ba0667d2016d1c6b5d4073fc47bc1.jpg"),
            content=(DIY_SAMPLES / "9d5ba0667d2016d1c6b5d4073fc47bc1.jpg").read_bytes(),
        )
        requests_mock.get(
            TRANSCRIBE_URL.format(3197, 77744),
            text=(DIY_SAMPLES / "transcribe_77744.html").read_text(),
        )
        requests_mock.get(
            IMAGE_URL.format("b6545daedf6d3bdbd07e73550f4c3b4f.jpg"),
            content=(DIY_SAMPLES / "b6545daedf6d3bdbd07e73550f4c3b4f.jpg").read_bytes(),
        )
        requests_mock.get(
            TRANSCRIBE_URL.format(3197, 77746),
            text=(DIY_SAMPLES / "transcribe_77746.html").read_text(),
        )
        requests_mock.get(
            IMAGE_URL.format("3e9d001c0769737e633f74ad2b4ce5e4.jpg"),
            content=(DIY_SAMPLES / "3e9d001c0769737e633f74ad2b4ce5e4.jpg").read_bytes(),
        )

        # Item 3373 with two transcribes
        requests_mock.get(
            ITEM_URL.format(3373),
            text=(DIY_SAMPLES / "item_3373.html").read_text(),
        )
        requests_mock.get(
            TRANSCRIBE_URL.format(3373, 83670),
            text=(DIY_SAMPLES / "transcribe_83670.html").read_text(),
        )
        requests_mock.get(
            IMAGE_URL.format("a0b0cc6bc95c54779a857edce4ea7f53.jpg"),
            content=(DIY_SAMPLES / "a0b0cc6bc95c54779a857edce4ea7f53.jpg").read_bytes(),
        )
        requests_mock.get(
            TRANSCRIBE_URL.format(3373, 83671),
            text=(DIY_SAMPLES / "transcribe_83671.html").read_text(),
        )
        requests_mock.get(
            IMAGE_URL.format("3cad08a3159fefadf4adee2debf8a7bd.jpg"),
            content=(DIY_SAMPLES / "3cad08a3159fefadf4adee2debf8a7bd.jpg").read_bytes(),
        )

        expected_requests = [
            # Collection page
            "http://s-lib017.lib.uiowa.edu/collections/show/13/",
            # Item 3197 with three transcribes
            "http://s-lib017.lib.uiowa.edu/items/show/3197/",
            "http://s-lib017.lib.uiowa.edu/transcribe/3197/77731/",
            "http://s-lib017.lib.uiowa.edu/files/original/9d5ba0667d2016d1c6b5d4073fc47bc1.jpg",
            "http://s-lib017.lib.uiowa.edu/transcribe/3197/77744/",
            "http://s-lib017.lib.uiowa.edu/files/original/b6545daedf6d3bdbd07e73550f4c3b4f.jpg",
            "http://s-lib017.lib.uiowa.edu/transcribe/3197/77746/",
            "http://s-lib017.lib.uiowa.edu/files/original/3e9d001c0769737e633f74ad2b4ce5e4.jpg",
            # Item 3373 with two transcribes
            "http://s-lib017.lib.uiowa.edu/items/show/3373/",
            "http://s-lib017.lib.uiowa.edu/transcribe/3373/83670/",
            "http://s-lib017.lib.uiowa.edu/files/original/a0b0cc6bc95c54779a857edce4ea7f53.jpg",
            "http://s-lib017.lib.uiowa.edu/transcribe/3373/83671/",
            "http://s-lib017.lib.uiowa.edu/files/original/3cad08a3159fefadf4adee2debf8a7bd.jpg",
        ]
    else:
        # Populate cache
        (output_dir / "html").mkdir(parents=True)
        for file_hash, filename in HASH_PAGE_MAPPING.items():
            shutil.copy(
                (DIY_SAMPLES / filename).with_suffix(".html"),
                (output_dir / "html" / file_hash).with_suffix(".html"),
            )

        for image_path in DIY_SAMPLES.rglob("*.jpg"):
            shutil.copy(
                image_path,
                (output_dir / image_path.name).with_suffix(".jpg"),
            )

        expected_requests = []

    Scraper(collection_id=13, output_dir=output_dir).run()

    # Check files
    expected_paths = [
        # Extracted data
        output_dir / "3197.json",
        output_dir / "3373.json",
        # Extracted images
        output_dir / "3cad08a3159fefadf4adee2debf8a7bd.jpg",
        output_dir / "3e9d001c0769737e633f74ad2b4ce5e4.jpg",
        output_dir / "9d5ba0667d2016d1c6b5d4073fc47bc1.jpg",
        output_dir / "a0b0cc6bc95c54779a857edce4ea7f53.jpg",
        output_dir / "b6545daedf6d3bdbd07e73550f4c3b4f.jpg",
        # Cache files
        output_dir / "html" / "2c87b9cc8e044a3c8b4170015b2da6aa.html",
        output_dir / "html" / "3759ad9c608ea220ebfc310a3017e511.html",
        output_dir / "html" / "5e308a96a027959822177632f121383c.html",
        output_dir / "html" / "6948ea08304931a3a46fe5c436270e8e.html",
        output_dir / "html" / "73bc940f8a4d4c69125f70f4036fe955.html",
        output_dir / "html" / "ba89de5fb79670953c5a0d2f857ced6f.html",
        output_dir / "html" / "ce0165e8f4d9e56df394c51b45423071.html",
        output_dir / "html" / "e93c0fcc8d91f2a9bb66006254925c07.html",
    ]
    assert (
        sorted(list(filter(methodcaller("is_file"), output_dir.rglob("*"))))
        == expected_paths
    )

    for file_path in expected_paths:
        match file_path.suffix:
            case ".html":
                file_name = Path(HASH_PAGE_MAPPING[file_path.stem]).with_suffix(".html")
                assert file_path.read_text() == (DIY_SAMPLES / file_name).read_text()
            case ".jpg":
                file_name = Path(file_path.name)
                assert file_path.read_bytes() == (DIY_SAMPLES / file_path).read_bytes()
            case _:
                file_name = Path(file_path.name)
                assert file_path.read_text() == (
                    DIY_SAMPLES / file_name
                ).read_text().replace("{output_dir}", str(output_dir))

    # Check requests
    assert sorted(map(attrgetter("url"), requests_mock.request_history)) == sorted(
        expected_requests
    )
