import pytest
from algokit_utils import (
    Account,
    get_localnet_default_account,
)
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.LifeCycleApp.client import (
    Create1Arg,
    Create2Arg,
    DeployCreate1Arg,
    DeployCreate2Arg,
    LifeCycleAppClient,
)


@pytest.fixture(scope="session")
def lifecycle_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> LifeCycleAppClient:
    account = get_localnet_default_account(algod_client)
    signer = AccountTransactionSigner(account.private_key)

    client = LifeCycleAppClient(
        algod_client=algod_client, signer=signer, template_values={"UPDATABLE": 1, "DELETABLE": 1}
    )
    return client


def test_create_bare(lifecycle_client: LifeCycleAppClient) -> None:
    lifecycle_client.create(args=None)
    response = lifecycle_client.hello(name="Bare")

    assert response.return_value == "Hello, Bare\n"


def test_create_1arg(lifecycle_client: LifeCycleAppClient) -> None:
    lifecycle_client.create(args=Create1Arg(greeting="Greetings"))
    response = lifecycle_client.hello(name="1 Arg")

    assert response.return_value == "Greetings, 1 Arg\n"


def test_create_2arg(lifecycle_client: LifeCycleAppClient) -> None:
    lifecycle_client.create(args=Create2Arg(greeting="Greetings", times=2))
    response = lifecycle_client.hello(name="2 Arg")

    assert response.return_value == "Greetings, 2 Arg\nGreetings, 2 Arg\n"


@pytest.fixture
def deploy_lifecycle_client(
    algod_client: AlgodClient, indexer_client: IndexerClient, new_account: Account
) -> LifeCycleAppClient:
    return LifeCycleAppClient(
        algod_client=algod_client,
        indexer_client=indexer_client,
        creator=new_account,
    )


def test_deploy_bare(deploy_lifecycle_client: LifeCycleAppClient) -> None:
    deploy_lifecycle_client.deploy(allow_delete=True, allow_update=True, create_args=None)
    assert deploy_lifecycle_client.app_client.app_id

    response = deploy_lifecycle_client.hello(name="Deploy Bare")

    assert response.return_value == "Hello, Deploy Bare\n"


def test_deploy_create_1arg(deploy_lifecycle_client: LifeCycleAppClient) -> None:
    deploy_lifecycle_client.deploy(
        allow_delete=True,
        allow_update=True,
        create_args=DeployCreate1Arg(args=Create1Arg(greeting="Deploy Greetings")),
    )
    assert deploy_lifecycle_client.app_client.app_id

    response = deploy_lifecycle_client.hello(name="1 Arg")

    assert response.return_value == "Deploy Greetings, 1 Arg\n"


def test_deploy_create_2arg(deploy_lifecycle_client: LifeCycleAppClient) -> None:
    deploy_lifecycle_client.deploy(
        allow_delete=True,
        allow_update=True,
        create_args=DeployCreate2Arg(
            args=Create2Arg(greeting="Deploy Greetings", times=2),
        ),
    )
    assert deploy_lifecycle_client.app_client.app_id

    response = deploy_lifecycle_client.hello(name="2 Arg")

    assert response.return_value == "Deploy Greetings, 2 Arg\nDeploy Greetings, 2 Arg\n"
