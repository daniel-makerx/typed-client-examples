import datetime
import math
import random

import algokit_utils
import algosdk
import pytest
from algokit_utils import get_localnet_default_account
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.VotingRoundApp.client import CreateArgs, DeployCallCreateAbiArgs, VotingRoundAppClient


def get_create_args(algod_client: AlgodClient) -> CreateArgs:
    quorum = math.ceil(random.randint(1, 9) * 1000)
    current_date = datetime.datetime.now()
    question_counts = [0 for i in range(0, 10)]
    vote_id = str(int(current_date.strftime("%Y%m%d%H%M%S")))

    health = algod_client.status()
    assert isinstance(health, dict)
    response = algod_client.block_info(health["last-round"])
    assert isinstance(response, dict)
    block = response["block"]
    block_ts = block["ts"]

    create_args = CreateArgs(
        vote_id=vote_id,
        metadata_ipfs_cid="cid",
        start_time=int(block_ts),
        end_time=int(block_ts) + 1000,
        quorum=quorum,
        snapshot_public_key=b"key",
        nft_image_url="ipfs://cid",
        option_counts=question_counts,
    )
    return create_args


def get_deploy_create_args(algod_client: AlgodClient) -> DeployCallCreateAbiArgs:
    sp = algod_client.suggested_params()
    sp.fee = algosdk.util.algos_to_microalgos(4)
    sp.flat_fee = True
    return DeployCallCreateAbiArgs(args=get_create_args(algod_client=algod_client), suggested_params=sp)


@pytest.fixture(scope="session")
def voting_round_app_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> VotingRoundAppClient:
    client = VotingRoundAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=get_localnet_default_account(algod_client),
    )
    # client.deploy(allow_delete=True, template_values={"VALUE": 1})
    return client


@pytest.fixture
def deploy_voting_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> VotingRoundAppClient:
    client = VotingRoundAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=get_localnet_default_account(algod_client),
    )
    client.deploy(allow_delete=True, create_args=get_deploy_create_args(algod_client=algod_client))

    return client


def test_close(deploy_voting_client: VotingRoundAppClient) -> None:
    deploy_voting_client.close()

    # assert response.return_value == "Hello, World"


def test_get_preconditions(deploy_voting_client: VotingRoundAppClient) -> None:
    response = deploy_voting_client.get_preconditions(signature=b"test")
    assert response.return_value == (0, 0, 0, 0)
    assert response.confirmed_round is None


def test_vote(deploy_voting_client: VotingRoundAppClient, algod_client: AlgodClient) -> None:
    from_account = algokit_utils.get_localnet_default_account(algod_client)
    sp = algod_client.suggested_params()
    sp.fee = 12000
    sp.flat_fee = True
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=deploy_voting_client.app_client.app_address,
        amt=200_000,
        note=b"Bootstrap payment",
        sp=algod_client.suggested_params(),
    )
    fund_min_bal_req = TransactionWithSigner(payment, deploy_voting_client.app_client.signer)
    signature = b"test"
    answer_ids = [1, 2, 3]
    response = deploy_voting_client.vote(
        fund_min_bal_req=fund_min_bal_req,
        signature=signature,
        answer_ids=answer_ids,
        transaction_parameters=algokit_utils.TransactionParameters(suggested_params=sp),
    )
    assert response.return_value is None


def test_create(voting_round_app_client: VotingRoundAppClient, algod_client: AlgodClient) -> None:
    voting_round_app_client.deploy(allow_delete=True, template_values={"VALUE": 1})
    voting_round_app_client.create(args=get_create_args(algod_client=algod_client))

    # assert response.return_value voting_round_app_client== "Hello, World"


def test_boostrap(voting_round_app_client: VotingRoundAppClient, algod_client: AlgodClient) -> None:
    voting_round_app_client.deploy(allow_delete=True, create_args=get_deploy_create_args(algod_client=algod_client))

    from_account = algokit_utils.get_localnet_default_account(voting_round_app_client.app_client.algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=voting_round_app_client.app_client.app_address,
        amt=(100000 * 2) + 1000 + 2500 + 400,
        note=b"Bootstrap payment",
        sp=voting_round_app_client.app_client.algod_client.suggested_params(),
    )

    voting_round_app_client.bootstrap(
        fund_min_bal_req=TransactionWithSigner(payment, voting_round_app_client.app_client.signer),
        transaction_parameters=algokit_utils.TransactionParameters(boxes=[(0, "V")]),
    )

    # assert result.confirmed_round is None
