import algokit_utils
import algosdk
import pytest
from algokit_utils import Account, OnUpdate
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.TestingApp.client import (
    CallCreateAbiArgs,
    CallDeleteAbiArgs,
    CallUpdateAbiArgs,
    DeployCallCreateAbiArgs,
    DeployCallDeleteAbiArgs,
    DeployCallUpdateAbiArgs,
    TestingAppClient,
)


@pytest.fixture()
def testingapp_client(
    algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account
) -> TestingAppClient:
    client = TestingAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=new_account,
    )

    return client


def test_call_abi(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    response = testingapp_client.call_abi(value="there")

    assert response.return_value == "Hello, there"
    assert response.confirmed_round is None


def test_call_abi_(testingapp_client: TestingAppClient, algod_client: AlgodClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    from_account = algokit_utils.get_localnet_default_account(algod_client)
    payment = algosdk.transaction.PaymentTxn(
        sender=from_account.address,
        receiver=testingapp_client.app_client.app_address,
        amt=200_000,
        note=b"Bootstrap payment",
        sp=algod_client.suggested_params(),
    )
    pay = TransactionWithSigner(payment, testingapp_client.app_client.signer)
    response = testingapp_client.call_abi_txn(txn=pay, value="there")

    assert response.return_value is None
    assert response.confirmed_round is None


def test_set_global(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    response = testingapp_client.set_global(int1=1, int2=2, bytes1="test", bytes2=bytes("test", encoding="utf8"))

    assert response.return_value is None


def test_set_local(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    testingapp_client.opt_in()
    response = testingapp_client.set_local(int1=1, int2=2, bytes1="test", bytes2=b"test")

    assert response.return_value is None


def test_set_box(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    algokit_utils.transfer(
        testingapp_client.app_client.algod_client,
        algokit_utils.TransferParameters(
            from_account=algokit_utils.get_localnet_default_account(testingapp_client.app_client.algod_client),
            to_address=testingapp_client.app_client.app_address,
            micro_algos=120000,
        ),
    )
    response = testingapp_client.set_box(
        name=b"test", value="test", transaction_parameters=algokit_utils.TransactionParameters(boxes=[(0, b"test")])
    )

    assert response.return_value is None


def test_error(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    with pytest.raises(Exception):
        testingapp_client.error()


def test_create_abi(algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account) -> None:
    testingapp_client = TestingAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=new_account,
        template_values={"VALUE": 1, "UPDATABLE": 1, "DELETABLE": 1},
    )

    response = testingapp_client.create_abi(input="test")

    assert response.return_value == "test"


def test_update_abi(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    response = testingapp_client.update_abi(input="test")

    assert response.return_value == "test"


def test_delete_abi(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    response = testingapp_client.delete_abi(input="test")

    assert response.return_value == "test"


def test_opt_in(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    response = testingapp_client.opt_in()

    assert response.confirmed_round


def test_get_global_state(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    testingapp_client.set_global(int1=1, int2=2, bytes1="test", bytes2=b"test")
    response = testingapp_client.get_global_state()

    assert response.bytes1 == "test"
    assert response.bytes2 == "test"
    assert response.int1 == 1
    assert response.int2 == 2
    assert response.value == 1


def test_get_local_state(testingapp_client: TestingAppClient) -> None:
    testingapp_client.deploy(
        template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp
    )
    testingapp_client.opt_in()
    testingapp_client.set_local(int1=1, int2=2, bytes1="test", bytes2=b"test")
    response = testingapp_client.get_local_state(account=None)

    assert response.local_bytes1 == "test"
    assert response.local_bytes2 == "test"
    assert response.local_int1 == 1
    assert response.local_int2 == 2


def test_deploy_create_1arg(testingapp_client: TestingAppClient) -> None:
    response = testingapp_client.deploy(
        allow_update=True,
        allow_delete=True,
        template_values={"VALUE": 1},
        create_args=DeployCallCreateAbiArgs(args=CallCreateAbiArgs(input="Deploy Greetings")),
        update_args=DeployCallUpdateAbiArgs(args=CallUpdateAbiArgs(input="Deploy Update")),
        delete_args=DeployCallDeleteAbiArgs(args=CallDeleteAbiArgs(input="Deploy Delete")),
    )
    assert testingapp_client.app_client.app_id
    assert isinstance(response.create_response, algokit_utils.ABITransactionResponse)
    assert response.create_response.return_value == "Deploy Greetings"

    testingapp_client.app_client.app_id = 0

    response = testingapp_client.deploy(
        allow_update=True,
        allow_delete=True,
        on_update=OnUpdate.UpdateApp,
        template_values={"VALUE": 2},
        create_args=DeployCallCreateAbiArgs(args=CallCreateAbiArgs(input="Deploy Greetings")),
        update_args=DeployCallUpdateAbiArgs(args=CallUpdateAbiArgs(input="Deploy Update")),
        delete_args=DeployCallDeleteAbiArgs(args=CallDeleteAbiArgs(input="Deploy Delete")),
    )
    assert testingapp_client.app_client.app_id
    assert isinstance(response.update_response, algokit_utils.ABITransactionResponse)
    assert response.update_response.return_value == "Deploy Update"

    testingapp_client.app_client.app_id = 0

    response = testingapp_client.deploy(
        allow_update=True,
        allow_delete=True,
        on_update=OnUpdate.ReplaceApp,
        template_values={"VALUE": 3},
        create_args=DeployCallCreateAbiArgs(args=CallCreateAbiArgs(input="Deploy Greetings")),
        update_args=DeployCallUpdateAbiArgs(args=CallUpdateAbiArgs(input="Deploy Update")),
        delete_args=DeployCallDeleteAbiArgs(args=CallDeleteAbiArgs(input="Deploy Delete")),
    )
    assert testingapp_client.app_client.app_id
    assert isinstance(response.delete_response, algokit_utils.ABITransactionResponse)
    assert response.delete_response.return_value == "Deploy Delete"
