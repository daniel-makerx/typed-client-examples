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
class CloseArgs(ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "close()ßvoid"


@dataclasses.dataclass(kw_only=True)
class GetPreconditionsArgs(ArgsBase[None]):
    signature: bytes

    @staticmethod
    def method() -> str:
        return "get_preconditions(signature)Tuple(int,int,int,int)"


@dataclasses.dataclass(kw_only=True)
class VoteArgs(ArgsBase[None]):
    fund_min_bal_req: TransactionWithSigner
    signature: bytes
    answer_ids: list[int]

    @staticmethod
    def method() -> str:
        return "vote(fund_min_bal_req,signature,answer_ids)void"


@dataclasses.dataclass(kw_only=True)
class CreateArgs(ArgsBase[None]):
    vote_id: str
    snapshot_public_key: bytes
    metadata_ipfs_cid: str
    start_time: int
    end_time: int
    option_counts: list[int]
    quorum: int
    nft_image_url: str

    @staticmethod
    def method() -> str:
        return "create(string,byte[],string,uint64,uint64,uint8[],uint64,string)void"


@dataclasses.dataclass(kw_only=True)
class BoostrapArgs(ArgsBase[None]):
    fund_min_bal_req: TransactionWithSigner

    @staticmethod
    def method() -> str:
        return "bootstrap(pay)void"


T = TypeVar("T")
TArgs = TypeVar("TArgs", bound=ArgsBase)


@dataclasses.dataclass(kw_only=True)
class TypedDeployCreateArgs(algokit_utils.DeployCreateCallArgs, Generic[TArgs]):
    args: TArgs


DeployCallCreateAbiArgs = TypedDeployCreateArgs[CreateArgs]


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


class VotingRoundAppClient:
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

    def close(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Returns void

        Calls the close() ABI method, using OnComplete = NoOp.

        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return void
        """
        args = CloseArgs()

        # call is used because the ABI method call config for close is no_op
        # from $.hints["close()void""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def get_preconditions(
        self,
        *,
        signature: bytes,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[(int, int, int, int)]:
        """Returns (uint,uint,uint,uint)

        Calls the close() ABI method, using OnComplete = NoOp.

        :params bytes signature:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return (int,int,int,int)
        """
        args = GetPreconditionsArgs(signature=signature)

        # call is used because the ABI method call config for close is no_op
        # from $.hints["get_preconditions(signature)Tuple(int,int,int,int)""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def vote(
        self,
        *,
        fund_min_bal_req: TransactionWithSigner,
        signature: bytes,
        answer_ids: list[int],
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Returns void

        Calls the close() ABI method, using OnComplete = NoOp.

        :params TransactionWithSigner fund_min_bal_req:
        :params bytes signature:
        :params list[int] answer_ids:
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return void
        """
        args = VoteArgs(fund_min_bal_req=fund_min_bal_req, signature=signature, answer_ids=answer_ids)

        # call is used because the ABI method call config for close is no_op
        # from $.hints["vote(fund_min_bal_req,signature,answer_ids)void"].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def create(  # from $.contract.methods[name="create"]
        self,
        *,
        args: CreateArgs,
        # vote_id: str,
        # snapshot_public_key: bytes,
        # metadata_ipfs_cid: str,
        # start_time: int,
        # end_time: int,
        # option_counts: int,
        # quorum: int,
        # nft_image_url: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the create(string,byte[],string,uint64,uint64,uint8[],uint64,string) ABI method, using OnComplete = NoOp.

        :params string vote_id
        :params byte[] snapshot_public_key
        :params string metadata_ipfs_cid
        :params uint64 start_time
        :params uint64 end_time
        :params uint8[] option_counts
        :params uint64 quorum
        :params string nft_image_url
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return void
        """
        args = CreateArgs(
            vote_id=args.vote_id,
            snapshot_public_key=args.snapshot_public_key,
            metadata_ipfs_cid=args.metadata_ipfs_cid,
            start_time=args.start_time,
            end_time=args.end_time,
            option_counts=args.option_counts,
            quorum=args.quorum,
            nft_image_url=args.nft_image_url,
        )
        # call is used because the ABI method call config for create is no_op
        # from $.hints["create(string,byte[],string,uint64,uint64,uint8[],uint64,string)void""].call_config
        return self.app_client.create(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    def bootstrap(  # from $.contract.methods[name="bootstrap"]
        self,
        *,
        fund_min_bal_req: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Returns {type}

        Calls the create(string,byte[],string,uint64,uint64,uint8[],uint64,string) ABI method, using OnComplete = NoOp.

        :params pay fund_min_bal_req
        :params TransactionParameters transaction_parameters: Any additional parameters for the transaction
        :return void
        """
        args = BoostrapArgs(fund_min_bal_req=fund_min_bal_req)
        # call is used because the ABI method call config for bootstrap is no_op
        # from $.hints["bootstrap(pay)void""].call_config
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=convert(transaction_parameters),
            **as_dict(args),
        )

    # def delete(  # from $.bare_call_config.delete_application == 'CALL'
    #     self,
    #     *,
    #     transaction_parameters: algokit_utils.TransactionParameters | None = None,
    # ) -> algokit_utils.TransactionResponse:
    #     return self.app_client.delete(
    #         call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
    #         transaction_parameters=convert(transaction_parameters),
    #     )

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
            create_args=convert_deploy_create(create_args),
            update_args=update_args,
            delete_args=delete_args,
        )
