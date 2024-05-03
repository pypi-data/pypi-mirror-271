import json
import logging
from operator import itemgetter
from pathlib import Path
from uuid import UUID

import requests
from apistar.exceptions import ErrorResponse

from arkindex import ArkindexClient
from scrapers.utils import ArkindexAPIClient, hash_image

logger = logging.getLogger(__name__)


def create_transcriptions(
    client: ArkindexClient,
    element_id: UUID,
    transcriptions: list[str],
    worker_run_id: str,
) -> None:
    """Add several transcriptions to the same element."""
    logger.debug(f"Creating transcriptions on element {element_id}...")

    try:
        client.request(
            "CreateTranscriptions",
            body={
                "transcriptions": [
                    {
                        "text": transcription,
                        "element_id": str(element_id),
                        "confidence": 1,
                    }
                    for transcription in transcriptions
                ],
                "worker_run_id": worker_run_id,
            },
        )
    except ErrorResponse as e:
        logger.error(
            f"Failed to create a transcription on element {element_id}: {e.status_code} - {e.content}"
        )


def publish_image(
    client: ArkindexClient, iiif_url: str, folder_path: Path, image_path: Path
) -> dict:
    if iiif_url:
        logger.debug(f"Publishing a IIIF image with url {iiif_url}...")

        try:
            return client.request("CreateIIIFURL", body={"url": iiif_url})
        except ErrorResponse as e:
            if e.status_code == 400 and "id" in e.content:
                return client.request("RetrieveImage", id=e.content["id"])
            logger.error(
                f"Failed to publish the IIIF image with url {iiif_url}: {e.status_code} - {e.content}"
            )

    elif image_path:
        image_path = folder_path / image_path

        logger.debug(f"Creating an image from the file located at {image_path}...")

        try:
            # Retrieve the S3 upload link
            image = client.request("CreateImage", body={"hash": hash_image(image_path)})

            # Upload the local image to S3
            requests.put(image["s3_put_url"], data=image_path.open("rb"))

            # Validate the image
            return client.request(
                "PartialUpdateImage", id=image["id"], body={"status": "checked"}
            )
        except ErrorResponse as e:
            if e.status_code == 400 and "id" in e.content:
                return client.request("RetrieveImage", id=e.content["id"])
            else:
                logger.error(
                    f"Failed to publish the image at path {image_path}: {e.status_code} - {e.content}"
                )


def publish_items(
    folder_path: Path,
    client: ArkindexClient,
    items: list,
    folder_id: UUID,
    corpus_id: UUID,
    type: str,
    worker_run_id: str,
) -> bool:
    logger.info(f"Publishing {len(items)} items in parent element {folder_id}...")

    for item in items:
        # Publish and validate the image
        image = publish_image(
            client, item.get("iiif_url"), folder_path, item.get("image_path")
        )
        if not image:
            return False

        # Create the page element
        page_element = create_element(
            client, type, item["name"], image["id"], corpus_id, folder_id, worker_run_id
        )
        if not page_element:
            return False

        # Add optional metadata on the page element
        metadata = item.get("metadata", [])
        if metadata:
            create_metadata(client, page_element["id"], metadata, worker_run_id)

        # Create an optional transcription on the page element
        transcriptions = item.get("transcriptions", [])
        if transcriptions:
            create_transcriptions(
                client, page_element["id"], transcriptions, worker_run_id
            )

    return True


def create_metadata(
    client: ArkindexClient, element_id: UUID, metadata: list, worker_run_id: str
) -> None:
    nb_metadata = len(metadata)

    # Remove duplicated metadata
    metadata = [
        {"type": md_type, "name": md_name, "value": md_value}
        # Build a set of value to remove duplicated metadata
        for md_type, md_name, md_value in sorted(
            set(map(itemgetter("type", "name", "value"), metadata))
        )
    ]
    if len(metadata) != nb_metadata:
        logger.warning(
            f"Found {nb_metadata - len(metadata)} duplicated metadata on element {element_id}..."
        )

    logger.debug(f"Adding {len(metadata)} metadata on element {element_id}...")

    try:
        client.request(
            "CreateMetaDataBulk",
            id=str(element_id),
            body={
                "metadata_list": metadata,
                "worker_run_id": worker_run_id,
            },
        )
    except ErrorResponse as e:
        logger.error(
            f"Failed to create {len(metadata)} metadata on element {element_id}: {e.status_code} - {e.content}"
        )


def create_element(
    client: ArkindexClient,
    type: str,
    name: str,
    image_id: str,
    corpus_id: UUID,
    parent_id: UUID,
    worker_run_id: str,
) -> dict:
    logger.info(f"Creating a {type} element named {name}...")

    try:
        extra = {}
        if image_id:
            extra["image"] = image_id

        return client.request(
            "CreateElement",
            body={
                "type": type,
                "name": name,
                "corpus": str(corpus_id),
                "parent": str(parent_id) if parent_id else None,
                "worker_run_id": worker_run_id,
                **extra,
            },
        )
    except ErrorResponse as e:
        logger.error(
            f"Failed to create {type} element {name}: {e.status_code} - {e.content}"
        )


def retrieve_parent_element(client: ArkindexClient, element_id: UUID) -> dict:
    logger.info(f"Retrieving parent element {element_id}...")

    try:
        return client.request("RetrieveElement", id=str(element_id))
    except ErrorResponse as e:
        logger.error(
            f"Failed to retrieve parent element {element_id}: {e.status_code} - {e.content}"
        )
        raise


def get_client(arkindex_api_url, arkindex_api_token):
    return ArkindexAPIClient(base_url=arkindex_api_url, token=arkindex_api_token)


def run(
    folder: Path,
    folder_type: str,
    page_type: str,
    report: Path,
    debug: bool,
    corpus_id: UUID,
    parent_id: UUID,
    arkindex_api_url: str,
    arkindex_api_token: str,
    worker_run_id: str,
) -> None:
    if debug:
        logger.setLevel(logging.DEBUG)

    if not worker_run_id:
        logger.error("Worker run ID not found")
        return

    # Arkindex auth
    client = get_client(arkindex_api_url, arkindex_api_token)

    if parent_id:
        corpus_id = retrieve_parent_element(client, parent_id)["corpus"]["id"]

    # Load or create the report file
    published_files = {}
    if report.exists():
        report_data = json.loads(report.read_text())
        published_files = (
            report_data.get("files", {})
            if report_data.get("arkindex_url") == arkindex_api_url
            else {}
        )
        logger.info(
            f"Found an existing report file with {len(published_files)} already published JSON file names"
        )
    else:
        logger.info(
            f"Creating a new report file to store published JSON file names at {report}"
        )

    # Browse all JSON files in provided folder
    try:
        for file_path in sorted(folder.iterdir()):
            if file_path.suffix.lower() != ".json":
                logger.debug(f"Skipping file at {file_path} as it is not a JSON file")
                continue

            if file_path.name in published_files:
                logger.info(
                    f"Skipping file at {file_path} as it was already published (cached)"
                )
                continue

            logger.info(
                f"--- Found a JSON file at {file_path} to import to Arkindex ---"
            )
            scraped = json.loads(file_path.read_text())

            # Create folder element
            folder_element = create_element(
                client,
                folder_type,
                scraped["name"],
                None,
                corpus_id,
                parent_id,
                worker_run_id,
            )
            if not folder_element:
                continue

            # Add metadata to the created folder
            metadata = scraped.get("metadata", [])
            if metadata:
                create_metadata(client, folder_element["id"], metadata, worker_run_id)

            # Publish all items to Arkindex
            success = True
            items = scraped.get("items", [])
            if items:
                success = publish_items(
                    folder,
                    client,
                    items,
                    folder_element["id"],
                    corpus_id,
                    page_type,
                    worker_run_id,
                )

            if success:
                published_files[file_path.name] = str(folder_element["id"])

    except Exception as e:
        logger.error(
            f"An error occurred while publishing scraped data to Arkindex: {e}"
        )

    finally:
        logger.info(f"Saving the names of published files in the report at {report}")
        report.write_text(
            json.dumps(
                {"arkindex_url": arkindex_api_url, "files": published_files}, indent=2
            )
        )
