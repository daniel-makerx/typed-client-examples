import pytest
from algokit_utils import Account, OnUpdate
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.VotingRoundApp.client import VotingRoundAppClient


@pytest.fixture()
def voting_round_app_client(
    algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account
) -> VotingRoundAppClient:
    client = VotingRoundAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=new_account,
    )
    return client


def test_close(voting_round_app_client: VotingRoundAppClient) -> None:
    voting_round_app_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, on_update=OnUpdate.UpdateApp
    )

    voting_round_app_client.close()

    # assert response.return_value == "Hello, World"
