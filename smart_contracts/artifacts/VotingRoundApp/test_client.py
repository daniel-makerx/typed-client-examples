import base64
import datetime
import math
import random

import algokit_utils
import algosdk
import pytest
from algokit_utils import Account, get_localnet_default_account
from algosdk.atomic_transaction_composer import AccountTransactionSigner, TransactionWithSigner
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from nacl.signing import SigningKey

from smart_contracts.artifacts.VotingRoundApp.client import CreateArgs, DeployCallCreateAbiArgs, VotingRoundAppClient


@pytest.fixture
def create_args(algod_client: AlgodClient, voter: tuple[Account, bytes]) -> CreateArgs:
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
        snapshot_public_key=algosdk.encoding.decode_address(voter[0].address),
        nft_image_url="ipfs://cid",
        option_counts=question_counts,
    )
    return create_args


@pytest.fixture
def deploy_create_args(algod_client: AlgodClient, create_args: CreateArgs) -> DeployCallCreateAbiArgs:
    sp = algod_client.suggested_params()
    sp.fee = algosdk.util.algos_to_microalgos(4)
    sp.flat_fee = True
    return DeployCallCreateAbiArgs(args=create_args, suggested_params=sp)


@pytest.fixture
def deploy_voting_client(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    new_account: Account,
    deploy_create_args: DeployCallCreateAbiArgs,
) -> VotingRoundAppClient:
    algokit_utils.transfer(
        client=algod_client,
        parameters=algokit_utils.TransferParameters(
            from_account=algokit_utils.get_localnet_default_account(algod_client),
            to_address=new_account.address,
            micro_algos=algosdk.util.algos_to_microalgos(10000),
        ),
    )

    client = VotingRoundAppClient(algod_client=algod_client, indexer_client=indexer_client, creator=new_account)
    client.deploy(allow_delete=True, create_args=deploy_create_args)

    return client


@pytest.fixture
def voter(algod_client: AlgodClient) -> tuple[Account, bytes]:
    voter = algosdk.account.generate_account()
    voter_account = Account(private_key=voter[0], address=voter[1])
    public_key = algosdk.encoding.decode_address(voter[1])
    private_key = base64.b64decode(voter[0])
    signing_key = SigningKey(private_key[: algosdk.constants.key_len_bytes])
    signed = signing_key.sign(public_key)
    signature = signed.signature
    algokit_utils.transfer(
        client=algod_client,
        parameters=algokit_utils.TransferParameters(
            from_account=algokit_utils.get_localnet_default_account(algod_client),
            to_address=voter_account.address,
            micro_algos=algosdk.util.algos_to_microalgos(100),
        ),
    )
    return voter_account, signature


def test_get_preconditions(
    deploy_voting_client: VotingRoundAppClient, algod_client: AlgodClient, voter: tuple[Account, bytes]
) -> None:
    signature = voter[1]
    sp = algod_client.suggested_params()
    sp.fee = 12000
    sp.flat_fee = True
    response = deploy_voting_client.get_preconditions(
        signature=signature,
        transaction_parameters=algokit_utils.TransactionParameters(
            boxes=[(0, algosdk.encoding.decode_address(voter[0].address))],
            suggested_params=sp,
            sender=voter[0].address,
            signer=AccountTransactionSigner(voter[0].private_key),
        ),
    )
    assert len(response.return_value) == 4


def test_vote(
    deploy_voting_client: VotingRoundAppClient, algod_client: AlgodClient, voter: tuple[Account, bytes]
) -> None:
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
    voter = algosdk.account.generate_account()
    sender_generate_account = algosdk.account.generate_account()
    sender_account = algokit_utils.models.Account(
        private_key=sender_generate_account[0], address=sender_generate_account[1]
    )
    transfer = algokit_utils.transfer(
        client=algod_client,
        parameters=algokit_utils.TransferParameters(
            from_account=sender_account,
            to_address=voter[1],
            micro_algos=algosdk.util.algos_to_microalgos(1),
            suggested_params=sp,
        ),
    )
    decoded = algosdk.encoding.decode_address(voter[1])
    signature = algosdk.logic.teal_sign(private_key=voter[0], contract_addr=transfer, data=decoded)
    signature = voter[1]
    answer_ids = [1, 2, 3]
    response = deploy_voting_client.vote(
        fund_min_bal_req=fund_min_bal_req,
        signature=signature,
        answer_ids=answer_ids,
        transaction_parameters=algokit_utils.TransactionParameters(suggested_params=sp),
    )
    assert response.return_value is None


def test_create(
    algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account, create_args: CreateArgs
) -> None:
    voting_round_app_client = VotingRoundAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=new_account,
        template_values={"VALUE": 1, "DELETABLE": 1},
    )

    sp = algod_client.suggested_params()
    sp.fee = algosdk.util.algos_to_microalgos(4)
    sp.flat_fee = True

    voting_round_app_client.create(
        args=create_args,
        transaction_parameters=algokit_utils.TransactionParameters(suggested_params=sp),
    )

    # assert response.return_value voting_round_app_client== "Hello, World"


def test_boostrap(
    deploy_voting_client: VotingRoundAppClient, algod_client: AlgodClient, deploy_create_args: DeployCallCreateAbiArgs
) -> None:
    from_account = algokit_utils.get_localnet_default_account(deploy_voting_client.app_client.algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=deploy_voting_client.app_client.app_address,
        amt=(100000 * 2) + 1000 + 2500 + 400,
        note=b"Bootstrap payment",
        sp=deploy_voting_client.app_client.algod_client.suggested_params(),
    )
    account = get_localnet_default_account(algod_client)
    signer = AccountTransactionSigner(account.private_key)

    deploy_voting_client.bootstrap(
        fund_min_bal_req=TransactionWithSigner(txn=payment, signer=signer),
        transaction_parameters=algokit_utils.TransactionParameters(boxes=[(0, "V")]),
    )

    # assert result.confirmed_round is None


def test_close(deploy_voting_client: VotingRoundAppClient, algod_client: AlgodClient) -> None:
    from_account = algokit_utils.get_localnet_default_account(deploy_voting_client.app_client.algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=deploy_voting_client.app_client.app_address,
        amt=(100000 * 2) + 1000 + 2500 + 400,
        note=b"Bootstrap payment",
        sp=deploy_voting_client.app_client.algod_client.suggested_params(),
    )
    account = get_localnet_default_account(algod_client)
    signer = AccountTransactionSigner(account.private_key)

    deploy_voting_client.bootstrap(
        fund_min_bal_req=TransactionWithSigner(txn=payment, signer=signer),
        transaction_parameters=algokit_utils.TransactionParameters(boxes=[(0, "V")]),
    )

    sp = deploy_voting_client.app_client.algod_client.suggested_params()
    sp.fee = algosdk.util.algos_to_microalgos(1)
    sp.flat_fee = True
    deploy_voting_client.close(transaction_parameters=algokit_utils.TransactionParameters(suggested_params=sp))
    # assert response.return_value == "Hello, World"
