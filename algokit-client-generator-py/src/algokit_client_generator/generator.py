import dataclasses
from collections.abc import Callable, Iterable, Sequence
from typing import Literal

from algokit_utils import ApplicationSpecification, OnCompleteActionName

from algokit_client_generator import utils
from algokit_client_generator.document import DocumentParts, Part
from algokit_client_generator.spec import ABIContractMethod, ContractMethod, get_contract_methods

ESCAPED_QUOTE = r"\""
SINGLE_QUOTE = '"'
TRIPLE_QUOTE = '"""'


@dataclasses.dataclass(kw_only=True)
class GenerationSettings:
    indent: str = "    "
    max_line_length: int = 80

    @property
    def indent_length(self) -> int:
        return len(self.indent)


def _get_unique_symbol_by_incrementing(
    existing_symbols: set[str], base_name: str, factory: Callable[[str, str], str]
) -> str:
    # TODO: better strategy for ensuring unique symbols
    suffix = 0
    while True:
        suffix_str = str(suffix) if suffix else ""
        symbol = factory(base_name, suffix_str)
        if symbol not in existing_symbols:
            existing_symbols.add(symbol)
            return symbol
        suffix += 1


class GenerateContext:
    def __init__(self, app_spec: ApplicationSpecification):
        self.app_spec = app_spec
        self.used_module_symbols = {
            "APP_SPEC",
            "_T",
            "_TResult",
            "_ArgsBase",
            "_as_dict",
        }
        self.used_client_symbols = {
            "__init__",
            "app_spec",
            "app_client",
            "no_op",
            "create",
            "update",
            "delete",
            "opt_in",
            "close_out",
            "clear_state",
            "deploy",
        }
        self.client_name = _get_unique_symbol_by_incrementing(
            self.used_module_symbols, f"{self.app_spec.contract.name}_client", utils.get_class_name
        )
        self.methods = get_contract_methods(app_spec)
        # calculate unique symbol names required for ABI methods
        for abi_method in self.methods.all_abi_methods:
            abi = abi_method.abi
            assert abi
            method_name = abi.method.name
            abi.args_class_name = _get_unique_symbol_by_incrementing(
                self.used_module_symbols, f"{method_name}_args", utils.get_class_name
            )
            if abi_method.call_config == "call" and "no_op" in abi_method.on_complete:
                abi.client_method_name = _get_unique_symbol_by_incrementing(
                    self.used_client_symbols, method_name, utils.get_method_name
                )
        self.disable_linting = True
        self.settings = GenerationSettings()


def lines(block: str) -> DocumentParts:
    yield from block.splitlines()


def generated_comment(context: GenerateContext) -> DocumentParts:
    yield "# This file was automatically generated by algokit-client-generator."
    yield "# DO NOT MODIFY IT BY HAND."


def disable_linting(context: GenerateContext) -> DocumentParts:
    yield "# flake8: noqa"  # this works for flake8 and ruff


def imports(context: GenerateContext) -> DocumentParts:
    yield from lines(
        """import dataclasses
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner, TransactionWithSigner"""
    )


def string_literal(value: str) -> str:
    return f'"{value}"'  # TODO escape quotes


def docstring(value: str) -> DocumentParts:
    yield Part.InlineMode
    yield TRIPLE_QUOTE
    value_lines = value.splitlines()
    last_idx = len(value_lines) - 1
    for idx, line in enumerate(value_lines):
        if idx == 0 and line.startswith(SINGLE_QUOTE):
            yield " "
        yield line
        if idx == last_idx and line.endswith(SINGLE_QUOTE):
            yield " "
        if idx != last_idx:
            yield Part.NewLine
    yield TRIPLE_QUOTE
    yield Part.RestoreLineMode


def typed_argument_class(contract_method: ContractMethod) -> DocumentParts:
    abi = contract_method.abi
    assert abi
    yield "@dataclasses.dataclass(kw_only=True)"
    yield f"class {abi.args_class_name}(_ArgsBase[{abi.python_type}]):"
    yield Part.IncIndent
    if abi.method.desc:
        yield from docstring(abi.method.desc)
        yield Part.Gap1
    if abi.args:
        for arg in abi.args:
            yield Part.InlineMode
            yield f"{arg.name}: {arg.python_type}"
            if arg.has_default:
                yield " | None = None"
            yield Part.RestoreLineMode
            if arg.desc:
                yield from docstring(arg.desc)
        yield Part.Gap1
    yield "@staticmethod"
    yield "def method() -> str:"
    yield Part.IncIndent
    yield Part.InlineMode
    yield "return "
    yield string_literal(abi.method.get_signature())
    yield Part.DecIndent
    yield Part.DecIndent
    yield Part.RestoreLineMode


def indented(code_block: str) -> DocumentParts:
    code_block = code_block.strip()
    current_indents = 0
    source_indent_size = 4
    for line in code_block.splitlines():
        indents = (len(line) - len(line.lstrip(" "))) / source_indent_size
        while indents > current_indents:
            yield Part.IncIndent
            current_indents += 1
        while indents < current_indents:
            yield Part.DecIndent
            current_indents -= 1
        yield line.strip()
    while current_indents > 0:
        yield Part.DecIndent
        current_indents -= 1


def typed_arguments(context: GenerateContext) -> DocumentParts:
    for method in context.methods.all_abi_methods:
        yield from typed_argument_class(method)
        yield Part.Gap2


def helpers(context: GenerateContext) -> DocumentParts:
    yield '_T = typing.TypeVar("_T")'
    if context.methods.has_abi_methods:
        yield '_TReturn = typing.TypeVar("_TReturn")'
        yield Part.Gap2
        yield from indented(
            """
class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ..."""
        )
    yield Part.Gap2
    yield from indented(
        """
def _as_dict(data: _T | None) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


def _convert_on_complete(on_complete: algokit_utils.OnCompleteActionName) -> algosdk.transaction.OnComplete:
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    return getattr(algosdk.transaction.OnComplete, on_complete_enum)"""
    )


def typed_client(context: GenerateContext) -> DocumentParts:
    yield from indented(
        f"""
class {context.client_name}:
    @typing.overload
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

    @typing.overload
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
        )"""
    )
    yield Part.Gap1
    yield Part.IncIndent
    yield from call_methods(context)
    yield from special_method(context, "create", context.methods.create)
    yield from special_method(context, "update", context.methods.update_application)
    yield from special_method(context, "delete", context.methods.delete_application)
    yield from special_method(context, "opt_in", context.methods.opt_in)
    yield from special_method(context, "close_out", context.methods.close_out)
    yield from clear_method(context)
    yield Part.Gap1
    yield from deploy_method(context)


def embed_app_spec(context: GenerateContext) -> DocumentParts:
    yield Part.InlineMode
    yield 'APP_SPEC = """'
    yield context.app_spec.to_json()
    yield '"""'
    yield Part.RestoreLineMode


def call_method(context: GenerateContext, contract_method: ABIContractMethod) -> DocumentParts:
    yield f"def {contract_method.client_method_name}("
    yield Part.IncIndent
    yield "self,"
    yield "*,"
    for arg in contract_method.args:
        yield Part.InlineMode
        yield f"{arg.name}: {arg.python_type}"
        if arg.has_default:
            yield " | None = None"
        yield ","
        yield Part.RestoreLineMode
    yield "transaction_parameters: algokit_utils.TransactionParameters | None = None,"
    yield Part.DecIndent
    yield f") -> algokit_utils.ABITransactionResponse[{contract_method.python_type}]:"
    yield Part.IncIndent
    # TODO: yield doc

    if not contract_method.args:
        yield f"args = {contract_method.args_class_name}()"
    else:
        yield f"args = {contract_method.args_class_name}(", Part.IncIndent
        for arg in contract_method.args:
            yield f"{arg.name}={arg.name},"
        yield Part.DecIndent, ")"

    yield from indented(
        """
return self.app_client.call(
    call_abi_method=args.method(),
    transaction_parameters=_as_dict(transaction_parameters),
    **_as_dict(args),
)"""
    )
    yield Part.DecIndent


def call_methods(context: GenerateContext) -> DocumentParts:
    for method in context.methods.no_op:
        if method.abi:
            yield from call_method(context, method.abi)
        else:
            yield from indented(
                """
def no_op(self) -> algokit_utils.TransactionResponse:
    return self.app_client.call(
        call_abi_method=False,
        transaction_parameters=_as_dict(transaction_parameters),
    )"""
            )
        yield Part.Gap1


def signature(
    context: GenerateContext, name: str, args: Sequence[str | DocumentParts], return_types: list[str]
) -> DocumentParts:
    yield f"def {name}("
    yield Part.IncIndent
    for arg in args:
        yield Part.InlineMode
        if isinstance(arg, str):
            yield f"{arg}"
        else:
            yield from arg
        yield ","
        yield Part.RestoreLineMode

    return_signature = f") -> {' | '.join(return_types)}:"

    if context.settings.indent_length + len(return_signature) < context.settings.max_line_length:
        yield Part.DecIndent, return_signature
    else:
        yield Part.DecIndent, ") -> ("
        yield Part.IncIndent
        for idx, return_type in enumerate(return_types):
            yield Part.InlineMode
            if idx:
                yield "| "
            yield return_type
            yield Part.RestoreLineMode
        yield Part.DecIndent, "):"


def on_complete_literals(on_completes: Iterable[OnCompleteActionName]) -> DocumentParts:
    yield 'on_complete: typing.Literal["'
    yield '", "'.join(on_completes)
    yield '"]'
    if "no_op" in on_completes:
        yield ' = "no_op"'


def special_typed_args(methods: list[ContractMethod]) -> DocumentParts:
    yield "args: "
    for idx, method in enumerate(m for m in methods if m.abi):
        assert method.abi
        assert method.abi.args_class_name
        if idx:
            yield " | "
        yield method.abi.args_class_name
    if any(not m.abi for m in methods):
        yield " | None = None"


def special_overload(
    context: GenerateContext,
    method_name: Literal["create", "update", "delete", "opt_in", "close_out"],
    method: ContractMethod,
) -> DocumentParts:
    yield "@typing.overload"
    args: list[str | DocumentParts] = ["self", "*"]

    if method.abi:
        args.append(f"args: {method.abi.args_class_name}")
        return_type = f"algokit_utils.ABITransactionResponse[{method.abi.python_type}]"
    else:
        args.append("args: typing.Literal[None] = None")
        return_type = "algokit_utils.TransactionResponse"
    if method_name == "create":
        args.append(on_complete_literals(method.on_complete))
        args.append("transaction_parameters: algokit_utils.CreateTransactionParameters | None = None")
    else:
        args.append("transaction_parameters: algokit_utils.TransactionParameters | None = None")
    yield from signature(context, method_name, args, [return_type])
    yield Part.IncIndent
    yield "..."
    yield Part.DecIndent


def special_method(
    context: GenerateContext,
    method_name: Literal["create", "update", "delete", "opt_in", "close_out"],
    methods: list[ContractMethod],
) -> DocumentParts:
    if not methods:
        return
    is_create = method_name == "create"
    has_bare = any(not m.abi for m in methods)
    bare_only = all(not m.abi for m in methods)
    # typed overloads
    if len(methods) > 1:
        for method in methods:
            yield from special_overload(context, method_name, method)
            yield Part.Gap1

    # signature
    args: list[str | DocumentParts] = ["self", "*"]
    if not bare_only:
        args.append(special_typed_args(methods))
    if is_create:
        args.append(on_complete_literals(sorted({c for m in methods for c in m.on_complete})))
        args.append("transaction_parameters: algokit_utils.CreateTransactionParameters | None = None")
    else:
        args.append("transaction_parameters: algokit_utils.TransactionParameters | None = None")

    return_types = []
    if has_bare:
        return_types.append("algokit_utils.TransactionResponse")

    return_types.extend(sorted(f"algokit_utils.ABITransactionResponse[{m.abi.python_type}]" for m in methods if m.abi))
    yield from signature(context, method_name, args, return_types)

    # implementation
    yield Part.IncIndent

    if is_create:
        yield "transaction_parameters_dict = _as_dict(transaction_parameters)"
        yield 'transaction_parameters_dict["on_complete"] = _convert_on_complete(on_complete)'
    yield f"return self.app_client.{method_name}("
    yield Part.IncIndent
    if bare_only:
        yield "call_abi_method=False,"
    else:
        yield "call_abi_method=args.method() if args else False,"
    if is_create:
        yield "transaction_parameters=transaction_parameters_dict,"
    else:
        yield "transaction_parameters=_as_dict(transaction_parameters),"
    if not bare_only:
        yield "**_as_dict(args),"
    yield Part.DecIndent
    yield ")"
    yield Part.DecIndent
    yield Part.Gap1


def clear_method(context: GenerateContext) -> DocumentParts:
    yield from indented(
        """
def clear_state(
    self,
    transaction_parameters: algokit_utils.TransactionParameters | None = None,
    app_args: list[bytes] | None = None,
) -> algokit_utils.TransactionResponse:
    return self.app_client.clear_state(_as_dict(transaction_parameters), app_args)"""
    )


def deploy_method(context: GenerateContext) -> DocumentParts:
    # TODO: typing
    yield from indented(
        """
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
    )"""
    )


def generate(context: GenerateContext) -> DocumentParts:
    if context.disable_linting:
        yield from disable_linting(context)
    yield from generated_comment(context)
    yield from imports(context)
    yield Part.Gap1
    yield from embed_app_spec(context)
    yield from helpers(context)
    yield Part.Gap2
    yield from typed_arguments(context)
    yield Part.Gap2
    yield from typed_client(context)
