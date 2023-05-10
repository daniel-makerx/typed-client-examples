import algokit_utils
import algosdk
import pytest
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.VotingRoundApp.client import VotingRoundAppClient

OPTION_COUNTS = [2]
TOTAL_OPTION_COUNTS = sum(OPTION_COUNTS)


@pytest.fixture(scope="session")
def voting_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> VotingRoundAppClient:
    client = VotingRoundAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=algokit_utils.get_localnet_default_account(algod_client),
        template_values={algokit_utils.DELETABLE_TEMPLATE_NAME[5:]: 0},  # TODO: add deploy to typed client
    )
    return client


@pytest.fixture(scope="session")
def last_block_ts(algod_client: AlgodClient) -> int:
    health = algod_client.status()
    assert isinstance(health, dict)
    response = algod_client.block_info(health["last-round"])
    assert isinstance(response, dict)
    block = response["block"]
    return block["ts"]


@pytest.fixture(scope="session")
def create_suggested_params(algod_client: AlgodClient) -> algosdk.transaction.SuggestedParams:
    sp = algod_client.suggested_params()
    sp.fee = algosdk.util.algos_to_microalgos(4)
    sp.flat_fee = True
    return sp


@pytest.fixture(scope="session")
def created_voting_client(
    last_block_ts: int,
    create_suggested_params: algosdk.transaction.SuggestedParams,
    voting_client: VotingRoundAppClient,
) -> VotingRoundAppClient:
    voting_client.create(
        vote_id="1",
        snapshot_public_key=b"000",
        metadata_ipfs_cid="cid",
        start_time=last_block_ts,
        end_time=last_block_ts + 1000,
        option_counts=OPTION_COUNTS,
        quorum=5,
        nft_image_url="nft",
        transaction_parameters=algokit_utils.CreateCallParameters(suggested_params=create_suggested_params),
    )
    return voting_client


def test_bootstrap(algod_client: AlgodClient, created_voting_client: VotingRoundAppClient) -> None:
    parameters = algokit_utils.CommonCallParameters(boxes=[(0, "V")])
    from_account = algokit_utils.get_localnet_default_account(algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=created_voting_client.app_client.app_address,
        amt=200_000 + 1_000 + 2_500 + 400 * (1 + 8 * TOTAL_OPTION_COUNTS),
        note=b"Bootstrap payment",
        sp=algod_client.suggested_params(),
    )
    payment_with_signer = TransactionWithSigner(payment, created_voting_client.app_client.signer)

    created_voting_client.bootstrap(fund_min_bal_req=payment_with_signer, transaction_parameters=parameters)
