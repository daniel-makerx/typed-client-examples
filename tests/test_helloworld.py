import pytest
from algokit_utils import (
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.HelloWorldApp.client import HelloWorldAppClient


@pytest.fixture(scope="session")
def helloworld_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> HelloWorldAppClient:
    client = HelloWorldAppClient(
        algod_client=algod_client, indexer_client=indexer_client, creator=get_localnet_default_account(algod_client)
    )
    client.app_client.deploy(allow_delete=True, allow_update=True)
    return client


def test_says_hello(helloworld_client: HelloWorldAppClient) -> None:
    assert helloworld_client.hello(name="World") == "Hello, World"
