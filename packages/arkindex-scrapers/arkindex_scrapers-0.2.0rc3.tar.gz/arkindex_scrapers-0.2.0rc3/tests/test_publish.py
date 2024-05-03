import json
import logging
import uuid
from pathlib import Path

import pytest

from scrapers.publish import create_metadata, run
from scrapers.utils import hash_image
from tests.test_diy import DIY_SAMPLES
from tests.test_eu_trans import EU_TRANS_SAMPLES

WORKER_RUN = "00000000-0000-0000-0000-000000000000"
CORPUS_ID = "11111111-1111-1111-1111-111111111111"
PARENT_ID = "22222222-2222-2222-2222-222222222222"


def build_api_calls_for_folder(
    arkindex_client,
    requests_mock,
    parent_id,
    folder_id,
    folder_name,
    folder_metadata,
    items,
    local_images=True,
):
    arkindex_client.add_response(
        "CreateElement",
        body={
            "type": "folder",
            "name": folder_name,
            "corpus": CORPUS_ID,
            "parent": parent_id,
            "worker_run_id": WORKER_RUN,
        },
        response={
            "id": folder_id,
        },
    )
    arkindex_client.add_response(
        "CreateMetaDataBulk",
        id=folder_id,
        body={"metadata_list": folder_metadata, "worker_run_id": WORKER_RUN},
        response={},
    )

    for item in items:
        image_id = str(uuid.uuid4())
        if local_images:
            # Uploading the image
            image_hash = hash_image(DIY_SAMPLES / item["image_path"])
            arkindex_client.add_response(
                "CreateImage",
                body={"hash": image_hash},
                response={
                    "id": image_id,
                    "s3_put_url": f"https://image-server.com/{image_hash}",
                },
            )
            requests_mock.put(f"https://image-server.com/{image_hash}")
            arkindex_client.add_response(
                "PartialUpdateImage",
                id=image_id,
                body={"status": "checked"},
                response={"id": image_id},
            )

            item["full_path"] = DIY_SAMPLES / item["image_path"]
        else:
            # Creating a IIIF URL
            arkindex_client.add_response(
                "CreateIIIFURL",
                body={"url": item["iiif_url"]},
                response={
                    "id": image_id,
                },
            )

        # Creating the child element
        page_id = str(uuid.uuid4())
        item["id"] = page_id

        arkindex_client.add_response(
            "CreateElement",
            body={
                "type": "page",
                "name": item["name"],
                "image": image_id,
                "corpus": CORPUS_ID,
                "parent": folder_id,
                "worker_run_id": WORKER_RUN,
            },
            response={
                "id": page_id,
            },
        )

        # Adding its optional metadata
        arkindex_client.add_response(
            "CreateMetaDataBulk",
            id=page_id,
            body={"metadata_list": item["metadata"], "worker_run_id": WORKER_RUN},
            response={},
        )

        # Adding its optional transcription
        arkindex_client.add_response(
            "CreateTranscriptions",
            body={
                "worker_run_id": WORKER_RUN,
                "transcriptions": [
                    {
                        "text": transcription,
                        "element_id": str(page_id),
                        "confidence": 1,
                    }
                    for transcription in item["transcriptions"]
                ],
            },
            response={},
        )

    return items


def build_logs_for_folder(
    json_path, folder_name, md_len, folder_id, items, local_images=True
):
    logs = [
        (
            logging.INFO,
            f"--- Found a JSON file at {json_path} to import to Arkindex ---",
        ),
        (logging.INFO, f"Creating a folder element named {folder_name}..."),
        (logging.DEBUG, f"Adding {md_len} metadata on element {folder_id}..."),
        (
            logging.INFO,
            f"Publishing {len(items)} items in parent element {folder_id}...",
        ),
    ]

    for item in items:
        if local_images:
            logs.append(
                (
                    logging.DEBUG,
                    f'Creating an image from the file located at {item["full_path"]}...',
                )
            )
        else:
            logs.append(
                (
                    logging.DEBUG,
                    f'Publishing a IIIF image with url {item["iiif_url"]}...',
                )
            )

        logs += [
            (logging.INFO, f'Creating a page element named {item["name"]}...'),
            (
                logging.DEBUG,
                f'Adding {len(item["metadata"])} metadata on element {item["id"]}...',
            ),
            (logging.DEBUG, f'Creating transcriptions on element {item["id"]}...'),
        ]

    return logs


def test_create_metadata_remove_duplicate(arkindex_client, caplog):
    logging.getLogger("scrapers.publish").setLevel(logging.DEBUG)

    element_id = "mock_element_id"
    metadata = [
        {"type": "reference", "name": "ID", "value": "39133712"},
        {"type": "reference", "name": "Language", "value": "fr"},
    ]

    # Add API call
    arkindex_client.add_response(
        "CreateMetaDataBulk",
        id=element_id,
        body={"metadata_list": metadata, "worker_run_id": WORKER_RUN},
        response={},
    )

    create_metadata(
        arkindex_client,
        element_id,
        metadata=metadata + [metadata[0]],
        worker_run_id=WORKER_RUN,
    )

    assert [(level, message) for _, level, message in caplog.record_tuples] == [
        (logging.WARNING, f"Found 1 duplicated metadata on element {element_id}..."),
        (logging.DEBUG, f"Adding {len(metadata)} metadata on element {element_id}..."),
    ]


@pytest.mark.parametrize(
    ("corpus_id", "parent_id"),
    [
        # Import in corpus
        (CORPUS_ID, None),
        # Import under parent in corpus
        (CORPUS_ID, PARENT_ID),
    ],
)
def test_publish_diy(
    mocker, arkindex_client, requests_mock, tmp_path, caplog, corpus_id, parent_id
):
    mocker.patch("scrapers.publish.get_client", return_value=arkindex_client)

    pre_logs = []
    if parent_id:
        arkindex_client.add_response(
            "RetrieveElement",
            id=parent_id,
            response={"id": parent_id, "corpus": {"id": corpus_id}},
        )
        pre_logs.append(
            (
                logging.INFO,
                "Retrieving parent element 22222222-2222-2222-2222-222222222222...",
            )
        )

    # Add API calls related to the first scraped JSON file
    folder_3197_id = str(uuid.uuid4())
    folder_3197_name = "Evelyn Birkby World War II scrapbook, 1942-1944"
    scraped_data_3197 = json.loads(Path(DIY_SAMPLES / "3197.json").read_text())
    updated_items_3197 = build_api_calls_for_folder(
        arkindex_client,
        requests_mock,
        parent_id,
        folder_3197_id,
        folder_3197_name,
        scraped_data_3197["metadata"],
        scraped_data_3197["items"],
        local_images=True,
    )

    # Add API calls related to the second scraped JSON file
    folder_3373_id = str(uuid.uuid4())
    folder_3373_name = "John N. Calhoun  family letters, August 1941-February 1946"
    scraped_data_3373 = json.loads(Path(DIY_SAMPLES / "3373.json").read_text())
    updated_items_3373 = build_api_calls_for_folder(
        arkindex_client,
        requests_mock,
        parent_id,
        folder_3373_id,
        folder_3373_name,
        scraped_data_3373["metadata"],
        scraped_data_3373["items"],
        local_images=True,
    )

    run(
        DIY_SAMPLES,
        "folder",
        "page",
        tmp_path / "report.json",
        True,
        uuid.UUID(corpus_id) if not parent_id else None,
        uuid.UUID(parent_id) if parent_id else None,
        "https://arkindex.teklia.com/api/v1/",
        "token",
        WORKER_RUN,
    )

    assert json.loads(Path(tmp_path / "report.json").read_text()) == {
        "arkindex_url": "https://arkindex.teklia.com/api/v1/",
        "files": {
            "3197.json": folder_3197_id,
            "3373.json": folder_3373_id,
        },
    }

    assert [(level, message) for _, level, message in caplog.record_tuples] == [
        *pre_logs,
        (
            logging.INFO,
            f"Creating a new report file to store published JSON file names at {tmp_path}/report.json",
        ),
        *build_logs_for_folder(
            f"{DIY_SAMPLES}/3197.json",
            folder_3197_name,
            2,
            folder_3197_id,
            updated_items_3197,
            local_images=True,
        ),
        *build_logs_for_folder(
            f"{DIY_SAMPLES}/3373.json",
            folder_3373_name,
            2,
            folder_3373_id,
            updated_items_3373,
            local_images=True,
        ),
        *[
            (
                logging.DEBUG,
                f"Skipping file at {DIY_SAMPLES}/{filename} as it is not a JSON file",
            )
            for filename in [
                "3cad08a3159fefadf4adee2debf8a7bd.jpg",
                "3e9d001c0769737e633f74ad2b4ce5e4.jpg",
                "9d5ba0667d2016d1c6b5d4073fc47bc1.jpg",
                "a0b0cc6bc95c54779a857edce4ea7f53.jpg",
                "b6545daedf6d3bdbd07e73550f4c3b4f.jpg",
                "collection_13.html",
                "item_3197.html",
                "item_3373.html",
                "transcribe_77731.html",
                "transcribe_77744.html",
                "transcribe_77746.html",
                "transcribe_83670.html",
                "transcribe_83671.html",
            ]
        ],
        (
            logging.INFO,
            f"Saving the names of published files in the report at {tmp_path}/report.json",
        ),
    ]


@pytest.mark.parametrize(
    ("corpus_id", "parent_id"),
    [
        # Import in corpus
        (CORPUS_ID, None),
        # Import under parent in corpus
        (CORPUS_ID, PARENT_ID),
    ],
)
def test_publish_eu_trans(
    mocker, arkindex_client, requests_mock, tmp_path, caplog, corpus_id, parent_id
):
    mocker.patch("scrapers.publish.get_client", return_value=arkindex_client)

    pre_logs = []
    if parent_id:
        arkindex_client.add_response(
            "RetrieveElement",
            id=parent_id,
            response={"id": parent_id, "corpus": {"id": corpus_id}},
        )
        pre_logs.append(
            (
                logging.INFO,
                "Retrieving parent element 22222222-2222-2222-2222-222222222222...",
            )
        )

    # Add API calls related to the first scraped JSON file
    folder_110349_id = str(uuid.uuid4())
    folder_110349_name = "FRAM - Lettre d'un fils à son père"
    scraped_data_110349 = json.loads(Path(EU_TRANS_SAMPLES / "110349.json").read_text())
    updated_items_110349 = build_api_calls_for_folder(
        arkindex_client,
        requests_mock,
        parent_id,
        folder_110349_id,
        folder_110349_name,
        scraped_data_110349["metadata"],
        scraped_data_110349["items"],
        local_images=False,
    )

    # Add API calls related to the second scraped JSON file
    folder_126760_id = str(uuid.uuid4())
    folder_126760_name = "FRAM - Charles DANGUEUGER |  originaire de Juziers."
    scraped_data_126760 = json.loads(Path(EU_TRANS_SAMPLES / "126760.json").read_text())
    updated_items_126760 = build_api_calls_for_folder(
        arkindex_client,
        requests_mock,
        parent_id,
        folder_126760_id,
        folder_126760_name,
        scraped_data_126760["metadata"],
        scraped_data_126760["items"],
        local_images=False,
    )

    run(
        EU_TRANS_SAMPLES,
        "folder",
        "page",
        tmp_path / "report.json",
        True,
        uuid.UUID(corpus_id) if not parent_id else None,
        uuid.UUID(parent_id) if parent_id else None,
        "https://arkindex.teklia.com/api/v1/",
        "token",
        WORKER_RUN,
    )

    assert json.loads(Path(tmp_path / "report.json").read_text()) == {
        "arkindex_url": "https://arkindex.teklia.com/api/v1/",
        "files": {
            "110349.json": folder_110349_id,
            "126760.json": folder_126760_id,
        },
    }

    assert [(level, message) for _, level, message in caplog.record_tuples] == [
        *pre_logs,
        (
            logging.INFO,
            f"Creating a new report file to store published JSON file names at {tmp_path}/report.json",
        ),
        *build_logs_for_folder(
            f"{EU_TRANS_SAMPLES}/110349.json",
            folder_110349_name,
            29,
            folder_110349_id,
            updated_items_110349,
            local_images=False,
        ),
        *build_logs_for_folder(
            f"{EU_TRANS_SAMPLES}/126760.json",
            folder_126760_name,
            25,
            folder_126760_id,
            updated_items_126760,
            local_images=False,
        ),
        *[
            (
                logging.DEBUG,
                f"Skipping file at {EU_TRANS_SAMPLES}/{filename} as it is not a JSON file",
            )
            for filename in [
                "item_1100686.html",
                "item_1100689.html",
                "item_1100691.html",
                "item_39133712.html",
                "no_stories.html",
                "stories.html",
                "story_110349.html",
                "story_126760.html",
            ]
        ],
        (
            logging.INFO,
            f"Saving the names of published files in the report at {tmp_path}/report.json",
        ),
    ]
