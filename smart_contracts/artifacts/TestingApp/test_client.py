import pytest
from algokit_utils import OnUpdate, get_localnet_default_account
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.TestingApp.client import TestingAppClient


@pytest.fixture(scope="session")
def testingapp_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> TestingAppClient:
    client = TestingAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=get_localnet_default_account(algod_client),
    )
    client.deploy(template_values={"VALUE": 1}, allow_delete=True, allow_update=True, on_update=OnUpdate.UpdateApp)
    return client


def test_call_abi(testingapp_client: TestingAppClient) -> None:
    response = testingapp_client.call_abi(value="there")

    assert response.return_value == "Hello, there"
    assert response.confirmed_round is None


# def test_lifecycle(algod_client: AlgodClient) -> None:
#     account = get_localnet_default_account(algod_client)
#     signer = AccountTransactionSigner(account.private_key)

#     helloworld_client = HelloWorldAppClient(
#         algod_client=algod_client, signer=signer, template_values={"UPDATABLE": 1, "DELETABLE": 1}
#     )

#     assert helloworld_client.create()
#     assert helloworld_client.update()

#     response = helloworld_client.hello(name="World")

#     assert response.return_value == "Hello, World"

#     assert helloworld_client.delete()
