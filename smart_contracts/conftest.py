import uuid
from pathlib import Path

import pytest
from algokit_utils import (
    Account,
    get_account,
    get_algod_client,
    get_indexer_client,
    is_localnet,
)
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from dotenv import load_dotenv


@pytest.fixture(autouse=True, scope="session")
def environment_fixture() -> None:
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)


@pytest.fixture(scope="session")
def algod_client() -> AlgodClient:
    client = get_algod_client()

    # you can remove this assertion to test on other networks,
    # included here to prevent accidentally running against other networks
    assert is_localnet(client)
    return client


@pytest.fixture(scope="session")
def indexer_client() -> IndexerClient:
    client = get_indexer_client()

    return client


@pytest.fixture
def new_account(algod_client: AlgodClient) -> Account:
    unique_name = str(uuid.uuid4()).replace("-", "")
    return get_account(algod_client, unique_name)
