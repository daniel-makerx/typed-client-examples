import dataclasses
import pathlib
from typing import Any, TypeVar, cast, overload

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner


@dataclasses.dataclass(kw_only=True)
class HelloArgs:
    name: str

    @staticmethod
    def method() -> str:
        return "hello(string)string"


@dataclasses.dataclass(kw_only=True)
class HelloCheckArgs:
    name: str

    @staticmethod
    def method() -> str:
        return "hello_world_check(string)void"


T = TypeVar("T")


def as_dict(data: T | None) -> dict[str, Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


def convert(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.CommonCallParametersDict | None:
    if transaction_parameters is None:
        return None
    # safe to cast this as the fields in TransactionParameters
    # are a subset of allowed keys in CommonCallParametersDict
    return cast(algokit_utils.CommonCallParametersDict, as_dict(transaction_parameters))


def convert_create(
    transaction_parameters: algokit_utils.CreateTransactionParameters | None,
) -> algokit_utils.CreateCallParametersDict | None:
    if transaction_parameters is None:
        return None
    # safe to cast this as the fields in CreateTransactionParameters
    # are a subset of allowed keys in CreateCallParametersDict
    return cast(algokit_utils.CreateCallParametersDict, as_dict(transaction_parameters))


class HelloWorldAppClient:
    @overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        ...

    @overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: "algosdk.v2client.indexer.IndexerClient | None" = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        app_spec_path = pathlib.Path(__file__).parent / "application.json"  # TODO: embed
        self.app_spec = algokit_utils.ApplicationSpecification.from_json(app_spec_path.read_text())

        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
        )

    def hello(  # from $.contract.methods[name="hello"]
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns Hello, {name}

        Calls the hello(name) ABI method, using OnComplete = NoOp.

        :params str name:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return str: The result of the call
        """
        args = HelloArgs(name=name)

        # call is used because the ABI method call config for hello is no_op
        # from $.hints["hello(string)string""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def hello_check_args(  # from $.contract.methods[name="hello_check_args"]
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Asserts {name} is "World"

        Calls the hello_check_args(name) ABI method, using OnComplete = NoOp.

        :params str name:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return str: The result of the call
        """
        args = HelloCheckArgs(name=name)

        # call is used because the ABI method call config for hello is no_op
        # from $.hints["hello(string)string""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def create(  # from $.bare_call_config.no_op == 'CREATE'
        self,
        *,
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.create(
            call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
            transaction_parameters=convert_create(transaction_parameters),
        )

    def delete(  # from $.bare_call_config.delete_application == 'CALL'
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.delete(
            call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
            transaction_parameters=convert(transaction_parameters),
        )

    def update(  # from $.bare_call_config.update_application == 'CALL'
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.update(
            call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
            transaction_parameters=convert(transaction_parameters),
        )

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=create_args,
            update_args=update_args,
            delete_args=delete_args,
        )
