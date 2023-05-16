import datetime
import math
import random

import algokit_utils
import algosdk
import pytest
from algokit_utils import Account, OnUpdate, get_localnet_default_account
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from artifacts.TestingApp.client import DeployCallCreateAbiArgs

from smart_contracts.artifacts.VotingRoundApp.client import CreateArgs, VotingRoundAppClient

# @pytest.fixture()
# def voting_round_app_client(
#     algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account
# ) -> VotingRoundAppClient:
#     client = VotingRoundAppClient(
#         algod_client=algod_client,
#         indexer_client=indexer_client,
#         creator=new_account,
#     )
#     return client


@pytest.fixture(scope="session")
def voting_round_app_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> VotingRoundAppClient:
    client = VotingRoundAppClient(
        template_values={"VALUE": 1},
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=get_localnet_default_account(algod_client),
    )
    client.deploy(allow_delete=True)
    return client


@pytest.fixture
def deploy_voting_client(
    algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account
) -> VotingRoundAppClient:
    client = VotingRoundAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=get_localnet_default_account(algod_client),
    )
    quorum = math.ceil(random.randint(1, 9) * 1000)
    current_date = datetime.datetime.now()
    question_counts = [0 for i in range(0, 10)]
    vote_id = str(int(current_date.strftime("%Y%m%d%H%M%S")))

    create_args = CreateArgs(
        vote_id=vote_id,
        metadata_ipfs_cid="cid",
        start_time=int(current_date.strftime("%H%M%S")),
        end_time=int(current_date.strftime("%H%M%S")) + 1000,
        quorum=quorum,
        snapshot_public_key=b"key",
        nft_image_url="ipfs://cid",
        option_counts=question_counts,
    )
    client.deploy(allow_delete=True, create_args=DeployCallCreateAbiArgs(args=create_args))
    return client


def test_close(deploy_voting_client: VotingRoundAppClient) -> None:
    deploy_voting_client.close()

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


def test_create(voting_round_app_client: VotingRoundAppClient) -> None:
    quorum = math.ceil(random.randint(1, 9) * 1000)
    current_date = datetime.datetime.now()
    question_counts = [0 for i in range(0, 10)]
    vote_id = str(int(current_date.strftime("%Y%m%d%H%M%S")))

    create_args = CreateArgs(
        vote_id=vote_id,
        metadata_ipfs_cid="cid",
        start_time=int(current_date.strftime("%H%M%S")),
        end_time=int(current_date.strftime("%H%M%S")) + 1000,
        quorum=quorum,
        snapshot_public_key=b"key",
        nft_image_url="ipfs://cid",
        option_counts=question_counts,
    )
    voting_round_app_client.create(args=create_args)

    # assert response.return_value == "Hello, World"


def test_boostrap(deploy_voting_client: VotingRoundAppClient) -> None:
    from_account = algokit_utils.get_localnet_default_account(deploy_voting_client.app_client.algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=deploy_voting_client.app_client.app_address,
        amt=200_000,
        note=b"Bootstrap payment",
        sp=deploy_voting_client.app_client.algod_client.suggested_params(),
    )

    result = deploy_voting_client.bootstrap(
        fund_min_bal_req=TransactionWithSigner(payment, deploy_voting_client.app_client.signer)
    )

    assert result.confirmed_round is None
