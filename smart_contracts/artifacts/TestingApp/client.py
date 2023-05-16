import dataclasses
import pathlib
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast, overload

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner, TransactionWithSigner

TReturn = TypeVar("TReturn")


class ArgsBase(ABC, Generic[TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


@dataclasses.dataclass(kw_only=True)
class CallAbiArgs(ArgsBase[str]):
    value: str

    @staticmethod
    def method() -> str:
        return "call_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class CallAbiTxnArgs(ArgsBase[string]):
    txn: TransactionWithSigner
    value: str

    @staticmethod
    def method() -> str:
        return "call_abi_txn(pay,string)string"


@dataclasses.dataclass(kw_only=True)
class CallSetGlobalArgs(ArgsBase[None]):
    int1: int
    int2: int
    bytes1: str
    bytes2: bytes

    @staticmethod
    def method() -> str:
        return "set_global(uint64,uint64,string,byte[4])void"


@dataclasses.dataclass(kw_only=True)
class CallSetLocalArgs(ArgsBase[None]):
    int1: int
    int2: int
    bytes1: str
    bytes2: bytes

    @staticmethod
    def method() -> str:
        return "set_local(uint64,uint64,string,byte[4])void"


@dataclasses.dataclass(kw_only=True)
class CallSetBoxArgs(ArgsBase[None]):
    name: bytes
    value: str

    @staticmethod
    def method() -> str:
        return "set_box(byte[4],string)void"


@dataclasses.dataclass(kw_only=True)
class CallErrorArgs(ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "error()void"


@dataclasses.dataclass(kw_only=True)
class CallCreateAbiArgs(ArgsBase[str]):
    input: str

    @staticmethod
    def method() -> str:
        return "create_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class CallUpdateAbiArgs(ArgsBase[str]):
    input: str

    @staticmethod
    def method() -> str:
        return "update_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class CallDeleteAbiArgs(ArgsBase[str]):
    input: str

    @staticmethod
    def method() -> str:
        return "delete_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class CallOptInArgs(ArgsBase[str]):
    @staticmethod
    def method() -> str:
        return "opt_in()void"


@dataclasses.dataclass(kw_only=True)
class GlobalState:
    bytes1: str
    bytes2: str
    int1: int
    int2: int
    value: int


@dataclasses.dataclass(kw_only=True)
class LocalState:
    local_bytes1: str
    local_bytes2: str
    local_int1: int
    local_int2: int


T = TypeVar("T")
TArgs = TypeVar("TArgs", bound=ArgsBase)


@dataclasses.dataclass(kw_only=True)
class TypedDeployCreateArgs(algokit_utils.DeployCreateCallArgs, Generic[TArgs]):
    args: TArgs


@dataclasses.dataclass(kw_only=True)
class TypedDeployArgs(algokit_utils.DeployCallArgs, Generic[TArgs]):
    args: TArgs


DeployCallCreateAbiArgs = TypedDeployCreateArgs[CallCreateAbiArgs]
DeployCallUpdateAbiArgs = TypedDeployArgs[CallUpdateAbiArgs]
DeployCallDeleteAbiArgs = TypedDeployArgs[CallDeleteAbiArgs]


def as_dict(data: T | None) -> dict[str, Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


def convert_deploy_create(
    deploy_args: algokit_utils.DeployCreateCallArgs | TypedDeployCreateArgs[TArgs] | None,
) -> algokit_utils.DeployCreateCallArgs | None:
    if deploy_args is None:
        return None

    if isinstance(deploy_args, TypedDeployCreateArgs):
        abi_args = deploy_args.args
        return algokit_utils.TypedCreateABICallArgs[TArgs](
            **as_dict(deploy_args),
            method=abi_args.method(),
        )
    return deploy_args


def convert_deploy(
    deploy_args: algokit_utils.DeployCallArgs | TypedDeployArgs[TArgs] | None,
) -> algokit_utils.DeployCallArgs | None:
    if deploy_args is None:
        return None

    if isinstance(deploy_args, TypedDeployArgs):
        abi_args = deploy_args.args
        return algokit_utils.TypedABICallArgs[TArgs](
            **as_dict(deploy_args),
            method=abi_args.method(),
        )
    return deploy_args


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


class TestingAppClient:
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

    def call_abi(  # from $.contract.methods[name="call_abi"]
        self,
        *,
        value: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the call_abi(value) ABI method, using OnComplete = NoOp.

        :params str value:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallAbiArgs(value=value)
        # call is used because the ABI method call config for call_abi is no_op
        # from $.hints["call_abi(string)string""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def call_abi_txn(  # from $.contract.methods[name="call_abi_txn"]
        self,
        *,
        txn: TransactionWithSigner,
        value: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the call_abi_txn(txn, value) ABI method, using OnComplete = NoOp.

        :params pay txn:
        :params str value:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallAbiTxnArgs(txn=txn, value=value)
        # call is used because the ABI method call config for call_abi_txn is no_op
        # from $.hints["call_abi_txn(txn,string)string""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    # TODO add validation to the bytes2 to check size is 4
    def set_global(  # from $.contract.methods[name="set_global"]
        self,
        *,
        int1: int,
        int2: int,
        bytes1: str,
        bytes2: bytes,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the set_global(uint64,uint64,string,byte[4]) ABI method, using OnComplete = NoOp.

        :params uint64 int1:
        :params uint64 int2:
        :params str bytes1:
        :params byte[4] bytes2:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallSetGlobalArgs(int1=int1, int2=int2, bytes1=bytes1, bytes2=bytes2)
        # call is used because the ABI method call config for set_global is no_op
        # from $.hints["set_global(uint64,uint64,string,byte[4])void""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    # TODO add validation to the bytes2 to check size is 4
    def set_local(  # from $.contract.methods[name="set_local"]
        self,
        *,
        int1: int,
        int2: int,
        bytes1: str,
        bytes2: bytes,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the set_local(uint64,uint64,string,byte[4]) ABI method, using OnComplete = NoOp.

        :params uint64 int1:
        :params uint64 int2:
        :params str bytes1:
        :params byte[4] bytes2:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallSetLocalArgs(int1=int1, int2=int2, bytes1=bytes1, bytes2=bytes2)
        # call is used because the ABI method call config for set_local is no_op
        # from $.hints["set_local(uint64,uint64,string,byte[4])void""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def set_box(  # from $.contract.methods[name="set_box"]
        self,
        *,
        name: bytes,
        value: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the set_box(byte[4],string) ABI method, using OnComplete = NoOp.

        :params byte[4] name:
        :params str value:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallSetBoxArgs(name=name, value=value)
        # call is used because the ABI method call config for set_box is no_op
        # from $.hints["set_box(byte[4],string)void""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def error(  # from $.contract.methods[name="error"]
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the set_box(byte[4],string) ABI method, using OnComplete = NoOp.

        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallErrorArgs()
        # call is used because the ABI method call config for error is no_op
        # from $.hints["error()void""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def create_abi(  # from $.contract.methods[name="create_abi"]
        self,
        *,
        input: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the create_abi(string) ABI method, using OnComplete = NoOp.

        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallCreateAbiArgs(input=input)
        # call is used because the ABI method call config for create_abi is no_op
        # from $.hints["create_abi(string)string""].call_config
        return self.app_client.create(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def update_abi(  # from $.contract.methods[name="update_abi"]
        self,
        *,
        input: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the update_abi(string) ABI method, using OnComplete = NoOp.

        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallUpdateAbiArgs(input=input)
        # call is used because the ABI method call config for update_abi is no_op
        # from $.hints["update_abi(string)string""].call_config
        return self.app_client.update(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def delete_abi(  # from $.contract.methods[name="delete_abi"]
        self,
        *,
        input: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the delete_abi(string) ABI method, using OnComplete = NoOp.

        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallDeleteAbiArgs(input=input)
        # call is used because the ABI method call config for delete_abi is no_op
        # from $.hints["delete_abi(string)string""].call_config
        return self.app_client.delete(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def opt_in(  # from $.contract.methods[name="opt_in"]
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the opt_in() ABI method, using OnComplete = NoOp.

        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return type: The result of the call
        """
        args = CallOptInArgs()
        # call is used because the ABI method call config for opt_in is no_op
        # from $.hints["opt_in()void""].call_config
        return self.app_client.opt_in(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def get_global_state(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> GlobalState:
        global_state = self.app_client.get_global_state()
        args = GlobalState(
            bytes1=global_state["bytes1"],
            bytes2=global_state["bytes2"],
            int1=global_state["int1"],
            int2=global_state["int2"],
            value=global_state["value"],
        )
        return args

    def get_local_state(
        self,
        *,
        account: str | None,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> LocalState:
        local_state = self.app_client.get_local_state(account=account)
        args = LocalState(
            local_bytes1=local_state["local_bytes1"],
            local_bytes2=local_state["local_bytes2"],
            local_int1=local_state["local_int1"],
            local_int2=local_state["local_int2"],
        )
        return args

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
        create_args: DeployCallCreateAbiArgs | algokit_utils.DeployCreateCallArgs | None = None,
        update_args: DeployCallUpdateAbiArgs | algokit_utils.DeployCallArgs | None = None,
        delete_args: DeployCallDeleteAbiArgs | algokit_utils.DeployCallArgs | None = None,
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
            create_args=convert_deploy_create(create_args),
            update_args=convert_deploy(update_args),
            delete_args=convert_deploy(delete_args),
        )
