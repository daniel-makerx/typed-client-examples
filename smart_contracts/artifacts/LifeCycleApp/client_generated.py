# flake8: noqa
import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, overload

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner, TransactionWithSigner

APP_SPEC = """{
    "hints": {
        "hello(string)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "create_1arg(string)string": {
            "call_config": {
                "no_op": "CREATE"
            }
        },
        "create_2arg(string,uint32)void": {
            "call_config": {
                "no_op": "CREATE"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSAxMApieXRlY2Jsb2NrIDB4NzQ2OTZkNjU3MyAweCAweDY3NzI2NTY1NzQ2OTZlNjcgMHgxNTFmN2M3NQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sOAp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweDAyYmVjZTExIC8vICJoZWxsbyhzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sNwp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGJjN2I2ZGY5IC8vICJjcmVhdGVfMWFyZyhzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sNgp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGQ4NjlmNjM2IC8vICJjcmVhdGVfMmFyZyhzdHJpbmcsdWludDMyKXZvaWQiCj09CmJueiBtYWluX2w1CmVycgptYWluX2w1Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCnN0b3JlIDIKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgppbnRjXzAgLy8gMApleHRyYWN0X3VpbnQzMgpzdG9yZSAzCmxvYWQgMgpsb2FkIDMKY2FsbHN1YiBjcmVhdGUyYXJnXzYKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDY6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBjcmVhdGUxYXJnXzUKc3RvcmUgMQpieXRlY18zIC8vIDB4MTUxZjdjNzUKbG9hZCAxCmNvbmNhdApsb2cKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDc6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBoZWxsb18zCnN0b3JlIDAKYnl0ZWNfMyAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CmJueiBtYWluX2wxNAp0eG4gT25Db21wbGV0aW9uCmludGNfMSAvLyBPcHRJbgo9PQpibnogbWFpbl9sMTMKdHhuIE9uQ29tcGxldGlvbgpwdXNoaW50IDQgLy8gVXBkYXRlQXBwbGljYXRpb24KPT0KYm56IG1haW5fbDEyCmVycgptYWluX2wxMjoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KYXNzZXJ0CmNhbGxzdWIgdXBkYXRlXzIKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDEzOgp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQphc3NlcnQKY2FsbHN1YiBiYXJlY3JlYXRlXzQKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDE0Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQphc3NlcnQKY2FsbHN1YiBiYXJlY3JlYXRlXzQKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBpbnRfdG9fYXNjaWkKaW50dG9hc2NpaV8wOgpwcm90byAxIDEKcHVzaGJ5dGVzIDB4MzAzMTMyMzMzNDM1MzYzNzM4MzkgLy8gIjAxMjM0NTY3ODkiCmZyYW1lX2RpZyAtMQppbnRjXzEgLy8gMQpleHRyYWN0MwpyZXRzdWIKCi8vIGl0b2EKaXRvYV8xOgpwcm90byAxIDEKZnJhbWVfZGlnIC0xCmludGNfMCAvLyAwCj09CmJueiBpdG9hXzFfbDUKZnJhbWVfZGlnIC0xCmludGNfMiAvLyAxMAovCmludGNfMCAvLyAwCj4KYm56IGl0b2FfMV9sNApieXRlY18xIC8vICIiCml0b2FfMV9sMzoKZnJhbWVfZGlnIC0xCmludGNfMiAvLyAxMAolCmNhbGxzdWIgaW50dG9hc2NpaV8wCmNvbmNhdApiIGl0b2FfMV9sNgppdG9hXzFfbDQ6CmZyYW1lX2RpZyAtMQppbnRjXzIgLy8gMTAKLwpjYWxsc3ViIGl0b2FfMQpiIGl0b2FfMV9sMwppdG9hXzFfbDU6CnB1c2hieXRlcyAweDMwIC8vICIwIgppdG9hXzFfbDY6CnJldHN1YgoKLy8gdXBkYXRlCnVwZGF0ZV8yOgpwcm90byAwIDAKdHhuIFNlbmRlcgpnbG9iYWwgQ3JlYXRvckFkZHJlc3MKPT0KLy8gdW5hdXRob3JpemVkCmFzc2VydApwdXNoaW50IFRNUExfVVBEQVRBQkxFIC8vIFRNUExfVVBEQVRBQkxFCi8vIENoZWNrIGFwcCBpcyB1cGRhdGFibGUKYXNzZXJ0CnJldHN1YgoKLy8gaGVsbG8KaGVsbG9fMzoKcHJvdG8gMSAxCmJ5dGVjXzEgLy8gIiIKYnl0ZWNfMSAvLyAiIgpzdG9yZSA0CmludGNfMCAvLyAwCnN0b3JlIDUKaGVsbG9fM19sMToKbG9hZCA1CmJ5dGVjXzAgLy8gInRpbWVzIgphcHBfZ2xvYmFsX2dldAo8CmJ6IGhlbGxvXzNfbDMKbG9hZCA0CmJ5dGVjXzIgLy8gImdyZWV0aW5nIgphcHBfZ2xvYmFsX2dldApjb25jYXQKcHVzaGJ5dGVzIDB4MmMyMCAvLyAiLCAiCmNvbmNhdApmcmFtZV9kaWcgLTEKZXh0cmFjdCAyIDAKY29uY2F0CnB1c2hieXRlcyAweDBhIC8vICJcbiIKY29uY2F0CnN0b3JlIDQKbG9hZCA1CmludGNfMSAvLyAxCisKc3RvcmUgNQpiIGhlbGxvXzNfbDEKaGVsbG9fM19sMzoKbG9hZCA0CmZyYW1lX2J1cnkgMApmcmFtZV9kaWcgMApsZW4KaXRvYgpleHRyYWN0IDYgMApmcmFtZV9kaWcgMApjb25jYXQKZnJhbWVfYnVyeSAwCnJldHN1YgoKLy8gYmFyZV9jcmVhdGUKYmFyZWNyZWF0ZV80Ogpwcm90byAwIDAKYnl0ZWNfMiAvLyAiZ3JlZXRpbmciCnB1c2hieXRlcyAweDQ4NjU2YzZjNmYgLy8gIkhlbGxvIgphcHBfZ2xvYmFsX3B1dApieXRlY18wIC8vICJ0aW1lcyIKaW50Y18xIC8vIDEKYXBwX2dsb2JhbF9wdXQKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBjcmVhdGVfMWFyZwpjcmVhdGUxYXJnXzU6CnByb3RvIDEgMQpieXRlY18xIC8vICIiCmJ5dGVjXzIgLy8gImdyZWV0aW5nIgpmcmFtZV9kaWcgLTEKZXh0cmFjdCAyIDAKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMCAvLyAidGltZXMiCmludGNfMSAvLyAxCmFwcF9nbG9iYWxfcHV0CmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApwdXNoYnl0ZXMgMHg1ZiAvLyAiXyIKY29uY2F0CmJ5dGVjXzAgLy8gInRpbWVzIgphcHBfZ2xvYmFsX2dldApjYWxsc3ViIGl0b2FfMQpjb25jYXQKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBjcmVhdGVfMmFyZwpjcmVhdGUyYXJnXzY6CnByb3RvIDIgMApieXRlY18yIC8vICJncmVldGluZyIKZnJhbWVfZGlnIC0yCmV4dHJhY3QgMiAwCmFwcF9nbG9iYWxfcHV0CmJ5dGVjXzAgLy8gInRpbWVzIgpmcmFtZV9kaWcgLTEKYXBwX2dsb2JhbF9wdXQKaW50Y18xIC8vIDEKcmV0dXJu",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDEKY2FsbHN1YiBjbGVhcl8wCmludGNfMCAvLyAxCnJldHVybgoKLy8gY2xlYXIKY2xlYXJfMDoKcHJvdG8gMCAwCmludGNfMCAvLyAxCnJldHVybg=="
    },
    "state": {
        "global": {
            "num_byte_slices": 1,
            "num_uints": 1
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "greeting": {
                    "type": "bytes",
                    "key": "greeting",
                    "descr": ""
                },
                "times": {
                    "type": "uint64",
                    "key": "times",
                    "descr": ""
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "LifeCycleApp",
        "methods": [
            {
                "name": "hello",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "create_1arg",
                "args": [
                    {
                        "type": "string",
                        "name": "greeting"
                    }
                ],
                "returns": {
                    "type": "string"
                },
                "desc": "ABI create method with 1 argument"
            },
            {
                "name": "create_2arg",
                "args": [
                    {
                        "type": "string",
                        "name": "greeting"
                    },
                    {
                        "type": "uint32",
                        "name": "times"
                    }
                ],
                "returns": {
                    "type": "void"
                },
                "desc": "ABI create method with 2 arguments"
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE",
        "opt_in": "CREATE",
        "update_application": "CALL"
    }
}"""
_T = TypeVar("_T")
_TReturn = TypeVar("_TReturn")


class _ArgsBase(ABC, Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


def _as_dict(data: _T | None) -> dict[str, Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


@dataclasses.dataclass(kw_only=True)
class HelloArgs(_ArgsBase[str]):
    name: str

    @staticmethod
    def method() -> str:
        return "hello(string)string"


@dataclasses.dataclass(kw_only=True)
class Create1ArgArgs(_ArgsBase[str]):
    """ABI create method with 1 argument"""

    greeting: str

    @staticmethod
    def method() -> str:
        return "create_1arg(string)string"


@dataclasses.dataclass(kw_only=True)
class Create2ArgArgs(_ArgsBase[None]):
    """ABI create method with 2 arguments"""

    greeting: str
    times: int

    @staticmethod
    def method() -> str:
        return "create_2arg(string,uint32)void"


class LifeCycleAppClient:
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
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        self.app_spec = APP_SPEC

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

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        args = HelloArgs(
            name=name,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def create(
        self,
        *,
        args: None | None | Create1ArgArgs | Create2ArgArgs = None,
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> (
        algokit_utils.TransactionResponse
        | algokit_utils.ABITransactionResponse[None]
        | algokit_utils.ABITransactionResponse[str]
    ):
        return self.app_client.create(
            call_abi_method=args.method() if args else False,
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def update(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.update(
            call_abi_method=False,
            transaction_parameters=_as_dict(transaction_parameters),
        )

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.clear_state(_as_dict(transaction_parameters), app_args)

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
