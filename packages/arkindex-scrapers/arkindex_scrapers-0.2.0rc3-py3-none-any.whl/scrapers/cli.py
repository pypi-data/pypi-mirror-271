import argparse
import logging
import os
import uuid
from pathlib import Path

from scrapers.diy import run as run_diy
from scrapers.eu_trans import run as run_eu_trans
from scrapers.publish import run as run_publish

logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO,
)


def main():
    parser = argparse.ArgumentParser(prog="scrapers")
    commands = parser.add_subparsers(help="Various website scrapers and other tools")

    # DIY History scraper
    diy = commands.add_parser(
        "diy",
        help="Get images and transcriptions from a DIY History collection",
    )
    diy.set_defaults(func=run_diy)
    diy.add_argument(
        "collection_id",
        type=int,
        help="ID of the collection.",
    )
    diy.add_argument(
        "-o",
        "--output_dir",
        required=True,
        type=Path,
        help="Path to the output directory.",
    )

    # Europeana Transcribathon scraper
    eu_trans = commands.add_parser(
        "eu-trans",
        help="Get images and transcriptions from Europeana Transcribathon stories.",
    )
    eu_trans.set_defaults(func=run_eu_trans)
    eu_trans.add_argument(
        "--story_id",
        type=str,
        default=None,
        help="ID of the story to extract. If set to None, all stories will be extracted.",
    )
    eu_trans.add_argument(
        "-o",
        "--output_dir",
        required=True,
        type=Path,
        help="Path to the output directory.",
    )

    # Publication to Arkindex
    publish = commands.add_parser(
        "publish",
        help="Publish scraped data saved in JSON files to Arkindex.",
    )
    publish.set_defaults(func=run_publish)
    publish.add_argument(
        "folder",
        type=Path,
        help="Path to the directory containing the JSON files describing scraped data.",
    )
    publish.add_argument(
        "--folder-type",
        type=str,
        default="folder",
        required=False,
        help="Type of the top level elements.",
    )
    publish.add_argument(
        "--page-type",
        type=str,
        default="page",
        required=False,
        help="Type of the child level elements.",
    )
    publish.add_argument(
        "--report",
        type=Path,
        default=Path("report.json"),
        required=False,
        help="Path to a JSON file to save the published JSON file names.",
    )
    publish.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose mode.",
    )

    group = publish.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--corpus-id",
        type=uuid.UUID,
        help="The UUID of the Arkindex corpus to publish in.",
    )
    group.add_argument(
        "--parent-id",
        type=uuid.UUID,
        help="The UUID of the Arkindex parent element to publish under.",
    )

    # Arkindex API Auth
    publish.add_argument(
        "--arkindex-api-url",
        type=str,
        default=os.getenv("ARKINDEX_API_URL"),
        required=False,
        help="URL of the Arkindex instance where the data should be published.",
    )
    publish.add_argument(
        "--arkindex-api-token",
        type=str,
        default=os.getenv("ARKINDEX_API_TOKEN"),
        required=False,
        help="API Token used to authenticate to the Arkindex instance.",
    )
    publish.add_argument(
        "--worker-run-id",
        type=str,
        default=os.getenv("ARKINDEX_WORKER_RUN_ID"),
        required=False,
        help="ID of the Worker Run used to publish elements and results on Arkindex.",
    )

    args = vars(parser.parse_args())
    if "func" in args:
        args.pop("func")(**args)
    else:
        parser.print_help()
