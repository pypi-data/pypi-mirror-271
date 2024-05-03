import os

import pytest

from arkindex.mock import MockApiClient


@pytest.fixture(autouse=True)
def _setup_environment(responses):
    """Setup needed environment variables"""

    # Allow accessing remote API schemas
    # defaulting to the prod environment
    schema_url = os.environ.get(
        "ARKINDEX_API_SCHEMA_URL",
        "https://arkindex.teklia.com/api/v1/openapi/?format=json",
    )
    responses.add_passthru(schema_url)

    # Set schema url in environment
    os.environ["ARKINDEX_API_SCHEMA_URL"] = schema_url


@pytest.fixture()
def arkindex_client():
    client = MockApiClient()
    yield client

    # Make sure all responses have been called
    assert len(client.responses) == 0
