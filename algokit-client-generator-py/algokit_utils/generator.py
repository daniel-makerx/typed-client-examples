import dataclasses
import sys
from collections.abc import Iterable
from enum import Enum
from pathlib import Path

from algosdk.abi import ABIType, Method, Returns

from algokit_utils import ApplicationSpecification


class Part(Enum):
    IncIndent = "IncIndent"
    DecIndent = "DecIndent"
    Indent = "Indent"
    NewLineMode = "NewLineMode"
    RestoreLineMode = "RestoreLineMode"
    InlineMode = "InlineMode"
    NewLine = "NewLine"
    FunctionGap = "FunctionGap"


DocumentPart = str | Part
DocumentParts = Iterable[DocumentPart]


def lines(block: str) -> DocumentParts:
    yield from block.splitlines()


def disable_linting() -> str:
    return "# flake8: noqa"  # this works for flake8 and ruff


def imports() -> DocumentParts:
    yield from lines(
        """import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast, overload

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner"""
    )


def string_literal(value: str) -> str:
    return f'"{value}"'  # TODO escape quotes


def docstring(value: str) -> DocumentParts:
    yield Part.InlineMode
    yield '"""'
    value_lines = value.splitlines()
    last_idx = len(value_lines) - 1
    for idx, line in enumerate(value_lines):
        yield line
        if idx == last_idx:
            # if end of doc string ends in ", need to add a separator before triple quote
            if line.endswith('"'):
                yield " "
        else:
            yield Part.NewLine
    yield '"""'
    yield Part.RestoreLineMode


def map_abi_type_to_python(abi_type: str | ABIType | Returns) -> str:
    abi_type_str = abi_type if isinstance(abi_type, str) else str(abi_type)
    return {
        "string": "str",
        "uint32": "int",
        "uint64": "int",
        "void": "None",
    }.get(abi_type_str, abi_type_str)


def typed_argument_class(method: Method) -> DocumentParts:
    arg_class_name = f"{method.name}Args"  # TODO: PascalCase name
    return_type = map_abi_type_to_python(method.returns)
    yield "@dataclasses.dataclass(kw_only=True)"
    yield f"class {arg_class_name}(ArgsBase[{return_type}]):"
    yield Part.IncIndent
    if method.desc:
        yield from docstring(method.desc)
    for arg in method.args:
        yield f"{arg.name}: {map_abi_type_to_python(arg.type)}"
        if arg.desc:
            yield from docstring(arg.desc)

    yield Part.FunctionGap
    yield "@staticmethod"
    yield "def method() -> str:"
    yield Part.IncIndent
    yield Part.InlineMode
    yield "return "
    yield string_literal(method.get_signature())
    yield Part.DecIndent
    yield Part.DecIndent
    yield Part.RestoreLineMode


def typed_arguments(methods: list[Method]) -> DocumentParts:
    if not methods:
        return
    yield 'TReturn = TypeVar("TReturn")'
    yield Part.FunctionGap
    yield """
class ArgsBase(ABC, Generic[TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...""".strip()
    yield Part.FunctionGap
    for method in methods:
        yield from typed_argument_class(method)
        yield Part.FunctionGap


def helpers() -> DocumentParts:
    yield """T = TypeVar("T")


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
    return cast(algokit_utils.CommonCallParametersDict, as_dict(transaction_parameters))


def convert_create(
    transaction_parameters: algokit_utils.CreateTransactionParameters | None,
) -> algokit_utils.CreateCallParametersDict | None:
    if transaction_parameters is None:
        return None
    return cast(algokit_utils.CreateCallParametersDict, as_dict(transaction_parameters))"""


def class_and_init(name: str) -> DocumentParts:
    app_client_name = f"{name}Client"
    yield f"""
class {app_client_name}:
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
        )""".strip()


def embed_app_spec(app_spec: ApplicationSpecification) -> DocumentParts:
    yield Part.InlineMode
    yield 'APP_SPEC = """'
    yield app_spec.to_json()
    yield '"""'
    yield Part.RestoreLineMode


def generate(app_spec: ApplicationSpecification) -> DocumentParts:
    yield disable_linting()
    yield from imports()
    yield Part.FunctionGap
    yield from typed_arguments(app_spec.contract.methods)
    yield Part.FunctionGap
    yield from helpers()
    yield Part.FunctionGap
    yield from embed_app_spec(app_spec)
    yield Part.FunctionGap
    yield from class_and_init(app_spec.contract.name)


@dataclasses.dataclass
class RenderContext:
    line_mode_stack: list[str]
    indent: str
    indent_inc: str
    last_part: DocumentPart | None
    last_rendered_part: str = ""

    @property
    def line_mode(self) -> str:
        return self.line_mode_stack[-1]


def convert_part_inner(part: DocumentPart, context: RenderContext) -> str | None:
    match part:
        case Part.IncIndent:
            context.indent += context.indent_inc
            return None
        case Part.DecIndent:
            context.indent = context.indent[: -len(context.indent_inc)]
            if not context.last_rendered_part.endswith("\n") and context.line_mode == "\n":
                return "\n"
            return None
        case Part.Indent:
            return context.indent
        case Part.NewLineMode:
            context.line_mode_stack.append("\n")
            return "\n"
        case Part.RestoreLineMode:
            context.line_mode_stack.pop()
            if context.line_mode == "\n":
                return "\n"
            return None
        case Part.InlineMode:
            context.line_mode_stack.append("")
            return None
        case Part.NewLine:
            return "\n"
        case Part.FunctionGap:
            if context.last_rendered_part.endswith("\n\n\n"):  # new lines already in place
                return None
            if context.last_rendered_part.endswith("\n\n"):
                return "\n"
            if context.last_rendered_part.endswith("\n"):
                return "\n\n"
            return "\n\n\n"
        case str():
            indent = context.indent if context.last_rendered_part.endswith("\n") else ""

            return f"{indent}{part}{context.line_mode}"
        case unknown:
            raise Exception(f"Unexpected part: {unknown}")


def convert_part(part: DocumentPart, context: RenderContext) -> str | None:
    result = convert_part_inner(part, context)
    context.last_part = part
    if result is not None:
        context.last_rendered_part = result
    return result


def render(parts: DocumentParts, indent_inc: str = "    ") -> str:
    context = RenderContext(line_mode_stack=["\n"], indent="", indent_inc=indent_inc, last_part=None)

    rendered_parts = [convert_part(p, context) for p in parts]
    return "".join(p for p in rendered_parts if p is not None)


input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])

app_spec = ApplicationSpecification.from_json(input_path.read_text())

output_path.write_text(render(generate(app_spec)))
