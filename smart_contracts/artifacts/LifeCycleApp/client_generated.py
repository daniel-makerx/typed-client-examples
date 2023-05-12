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
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSAxMApieXRlY2Jsb2NrIDB4NzQ2OTZkNjU3MyAweCAweDY3NzI2NTY1NzQ2OTZlNjcgMHgxNTFmN2M3NQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sOAp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweDAyYmVjZTExIC8vICJoZWxsbyhzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sNwp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGJjN2I2ZGY5IC8vICJjcmVhdGVfMWFyZyhzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sNgp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGQ4NjlmNjM2IC8vICJjcmVhdGVfMmFyZyhzdHJpbmcsdWludDMyKXZvaWQiCj09CmJueiBtYWluX2w1CmVycgptYWluX2w1Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCnN0b3JlIDIKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgppbnRjXzAgLy8gMApleHRyYWN0X3VpbnQzMgpzdG9yZSAzCmxvYWQgMgpsb2FkIDMKY2FsbHN1YiBjcmVhdGUyYXJnXzYKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDY6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBjcmVhdGUxYXJnXzUKc3RvcmUgMQpieXRlY18zIC8vIDB4MTUxZjdjNzUKbG9hZCAxCmNvbmNhdApsb2cKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDc6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBoZWxsb18zCnN0b3JlIDAKYnl0ZWNfMyAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CmJueiBtYWluX2wxMgp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNCAvLyBVcGRhdGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sMTEKZXJyCm1haW5fbDExOgp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiB1cGRhdGVfMgppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMTI6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CmFzc2VydApjYWxsc3ViIGJhcmVjcmVhdGVfNAppbnRjXzEgLy8gMQpyZXR1cm4KCi8vIGludF90b19hc2NpaQppbnR0b2FzY2lpXzA6CnByb3RvIDEgMQpwdXNoYnl0ZXMgMHgzMDMxMzIzMzM0MzUzNjM3MzgzOSAvLyAiMDEyMzQ1Njc4OSIKZnJhbWVfZGlnIC0xCmludGNfMSAvLyAxCmV4dHJhY3QzCnJldHN1YgoKLy8gaXRvYQppdG9hXzE6CnByb3RvIDEgMQpmcmFtZV9kaWcgLTEKaW50Y18wIC8vIDAKPT0KYm56IGl0b2FfMV9sNQpmcmFtZV9kaWcgLTEKaW50Y18yIC8vIDEwCi8KaW50Y18wIC8vIDAKPgpibnogaXRvYV8xX2w0CmJ5dGVjXzEgLy8gIiIKaXRvYV8xX2wzOgpmcmFtZV9kaWcgLTEKaW50Y18yIC8vIDEwCiUKY2FsbHN1YiBpbnR0b2FzY2lpXzAKY29uY2F0CmIgaXRvYV8xX2w2Cml0b2FfMV9sNDoKZnJhbWVfZGlnIC0xCmludGNfMiAvLyAxMAovCmNhbGxzdWIgaXRvYV8xCmIgaXRvYV8xX2wzCml0b2FfMV9sNToKcHVzaGJ5dGVzIDB4MzAgLy8gIjAiCml0b2FfMV9sNjoKcmV0c3ViCgovLyB1cGRhdGUKdXBkYXRlXzI6CnByb3RvIDAgMAp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CnB1c2hpbnQgVE1QTF9VUERBVEFCTEUgLy8gVE1QTF9VUERBVEFCTEUKLy8gQ2hlY2sgYXBwIGlzIHVwZGF0YWJsZQphc3NlcnQKcmV0c3ViCgovLyBoZWxsbwpoZWxsb18zOgpwcm90byAxIDEKYnl0ZWNfMSAvLyAiIgpieXRlY18xIC8vICIiCnN0b3JlIDQKaW50Y18wIC8vIDAKc3RvcmUgNQpoZWxsb18zX2wxOgpsb2FkIDUKYnl0ZWNfMCAvLyAidGltZXMiCmFwcF9nbG9iYWxfZ2V0CjwKYnogaGVsbG9fM19sMwpsb2FkIDQKYnl0ZWNfMiAvLyAiZ3JlZXRpbmciCmFwcF9nbG9iYWxfZ2V0CmNvbmNhdApwdXNoYnl0ZXMgMHgyYzIwIC8vICIsICIKY29uY2F0CmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApjb25jYXQKcHVzaGJ5dGVzIDB4MGEgLy8gIlxuIgpjb25jYXQKc3RvcmUgNApsb2FkIDUKaW50Y18xIC8vIDEKKwpzdG9yZSA1CmIgaGVsbG9fM19sMQpoZWxsb18zX2wzOgpsb2FkIDQKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBiYXJlX2NyZWF0ZQpiYXJlY3JlYXRlXzQ6CnByb3RvIDAgMApieXRlY18yIC8vICJncmVldGluZyIKcHVzaGJ5dGVzIDB4NDg2NTZjNmM2ZiAvLyAiSGVsbG8iCmFwcF9nbG9iYWxfcHV0CmJ5dGVjXzAgLy8gInRpbWVzIgppbnRjXzEgLy8gMQphcHBfZ2xvYmFsX3B1dAppbnRjXzEgLy8gMQpyZXR1cm4KCi8vIGNyZWF0ZV8xYXJnCmNyZWF0ZTFhcmdfNToKcHJvdG8gMSAxCmJ5dGVjXzEgLy8gIiIKYnl0ZWNfMiAvLyAiZ3JlZXRpbmciCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dApieXRlY18wIC8vICJ0aW1lcyIKaW50Y18xIC8vIDEKYXBwX2dsb2JhbF9wdXQKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCnB1c2hieXRlcyAweDVmIC8vICJfIgpjb25jYXQKYnl0ZWNfMCAvLyAidGltZXMiCmFwcF9nbG9iYWxfZ2V0CmNhbGxzdWIgaXRvYV8xCmNvbmNhdApmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIGNyZWF0ZV8yYXJnCmNyZWF0ZTJhcmdfNjoKcHJvdG8gMiAwCmJ5dGVjXzIgLy8gImdyZWV0aW5nIgpmcmFtZV9kaWcgLTIKZXh0cmFjdCAyIDAKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMCAvLyAidGltZXMiCmZyYW1lX2RpZyAtMQphcHBfZ2xvYmFsX3B1dAppbnRjXzEgLy8gMQpyZXR1cm4=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
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


def _convert(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.CommonCallParametersDict | algokit_utils.CreateCallParametersDict | None:
    if transaction_parameters is None:
        return None
    return _as_dict(transaction_parameters)


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
        args = HelloArgs(name=name,)
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert(transaction_parameters),
            **_as_dict(args),
        )

    def create(
        self,
        *,
        args: None | Create1ArgArgs | Create2ArgArgs = None,
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> (
        algokit_utils.TransactionResponse
        | algokit_utils.ABITransactionResponse[None]
        | algokit_utils.ABITransactionResponse[str]
    ):
        return self.app_client.create(
            call_abi_method=args.method() if args else False,
            transaction_parameters=_convert(transaction_parameters),
            **_as_dict(args)
        )

    def update(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.update(
            call_abi_method=False,
            transaction_parameters=_convert(transaction_parameters),
        )

