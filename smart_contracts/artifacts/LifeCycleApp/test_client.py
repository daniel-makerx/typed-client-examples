from pathlib import Path

from algokit_utils import (
    ApplicationClient,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient


def test_lifecycle_client_create_2arg(algod_client: AlgodClient, indexer_client: IndexerClient) -> None:
    app_spec = Path(__file__).parent / "application.json"
    lifecycle_client = ApplicationClient(
        algod_client=algod_client,
        app_spec=app_spec,
        indexer_client=indexer_client,
        creator=get_localnet_default_account(algod_client),
        template_values={"UPDATABLE": 1, "DELETABLE": 1},
    )
    lifecycle_client.create("create_2arg", greeting="Greetings", times=2)
    response = lifecycle_client.call("hello", name="World")

    assert response.return_value == "Greetings, World\nGreetings, World\n"
