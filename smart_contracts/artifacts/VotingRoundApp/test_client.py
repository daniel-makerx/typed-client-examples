import algokit_utils
import algosdk
import pytest
from algokit_utils import Account, OnUpdate
from algosdk.atomic_transaction_composer import TransactionWithSigner
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
    voting_round_app_client.deploy(template_values={"VALUE": 1}, allow_delete=True, on_update=OnUpdate.UpdateApp)
    voting_round_app_client.close()

    # assert response.return_value == "Hello, World"


def test_get_preconditions(voting_round_app_client: VotingRoundAppClient) -> None:
    voting_round_app_client.deploy(template_values={"VALUE": 1}, allow_delete=True, on_update=OnUpdate.UpdateApp)
    response = voting_round_app_client.get_preconditions(signature=b"test")
    assert response.return_value == (0, 0, 0, 0)
    assert response.confirmed_round is None


def test_vote(voting_round_app_client: VotingRoundAppClient, algod_client: AlgodClient) -> None:
    voting_round_app_client.deploy(template_values={"VALUE": 1}, allow_delete=True, on_update=OnUpdate.UpdateApp)
    from_account = algokit_utils.get_localnet_default_account(algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=voting_round_app_client.app_client.app_address,
        amt=200_000,
        note=b"Bootstrap payment",
        sp=algod_client.suggested_params(),
    )
    fund_min_bal_req = TransactionWithSigner(payment, voting_round_app_client.app_client.signer)
    signature = b"test"
    answer_ids = [1, 2, 3]
    response = voting_round_app_client.vote(
        fund_min_bal_req=fund_min_bal_req, signature=signature, answer_ids=answer_ids
    )
    assert response.return_value is None
