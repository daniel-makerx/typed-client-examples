import dataclasses
import re
import sys
from collections.abc import Iterable
from enum import Enum
from pathlib import Path

from algosdk.abi import ABIType, Method, Returns

from algokit_utils import ApplicationSpecification, CallConfig, MethodConfigDict


class Part(Enum):
    IncIndent = "IncIndent"
    DecIndent = "DecIndent"
    Indent = "Indent"
    NewLineMode = "NewLineMode"
    RestoreLineMode = "RestoreLineMode"
    InlineMode = "InlineMode"
    NewLine = "NewLine"
    Gap1 = "Gap1"
    Gap2 = "Gap2"


DocumentPart = str | Part
DocumentParts = Iterable[DocumentPart]


@dataclasses.dataclass(kw_only=True)
class ContractMethods:
    no_op: list[Method | None] = dataclasses.field(default_factory=list)
    create: list[Method | None] = dataclasses.field(default_factory=list)
    update_application: list[Method | None] = dataclasses.field(default_factory=list)
    delete_application: list[Method | None] = dataclasses.field(default_factory=list)
    opt_in: list[Method | None] = dataclasses.field(default_factory=list)
    close_out: list[Method | None] = dataclasses.field(default_factory=list)

    def add_method(self, method: Method | None, method_config: MethodConfigDict) -> None:
        for on_complete, call_config in method_config.items():
            if call_config & CallConfig.CALL != CallConfig.NEVER:
                collection = getattr(self, on_complete)
                collection.append(method)
            if call_config & CallConfig.CREATE != CallConfig.NEVER:
                self.create.append(method)


def get_contract_methods(app_spec: ApplicationSpecification) -> ContractMethods:
    result = ContractMethods()
    result.add_method(None, app_spec.bare_call_config)

    for method in app_spec.contract.methods:
        hints = app_spec.hints[method.get_signature()]
        result.add_method(method, hints.call_config)

    return result


def get_parts(value: str) -> list[str]:
    return re.findall("[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]", value)


# TODO handle overloads
def get_class_name(name: str) -> str:
    parts = get_parts(name)
    return "".join(p.title() for p in parts)


def get_method_name(name: str) -> str:
    return "_".join(p.lower() for p in get_parts(name))


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
    # TODO: better type mapping
    abi_type_str = abi_type if isinstance(abi_type, str) else str(abi_type)
    return {
        "string": "str",
        "uint32": "int",
        "uint64": "int",
        "void": "None",
    }.get(abi_type_str, abi_type_str)


def typed_argument_class(method: Method) -> DocumentParts:
    arg_class_name = get_class_name(f"{method.name}Args")
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

    yield Part.Gap2
    yield "@staticmethod"
    yield "def method() -> str:"
    yield Part.IncIndent
    yield Part.InlineMode
    yield "return "
    yield string_literal(method.get_signature())
    yield Part.DecIndent
    yield Part.DecIndent
    yield Part.RestoreLineMode


def indented(code_block: str) -> DocumentParts:
    code_block = code_block.strip()
    current_indents = 0
    indent_size = 4  # TODO: get from render context
    for line in code_block.splitlines():
        indents = (len(line) - len(line.lstrip(" "))) / indent_size
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


def typed_arguments(methods: ContractMethods) -> DocumentParts:
    if not methods:
        return
    yield 'TReturn = TypeVar("TReturn")'
    yield Part.Gap2
    yield from indented(
        """
class ArgsBase(ABC, Generic[TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ..."""
    )
    yield Part.Gap2
    for method_group in methods.__dict__.values():
        for method in method_group:
            if method is None:
                continue
            yield from typed_argument_class(method)
            yield Part.Gap2


def helpers() -> DocumentParts:
    yield from indented(
        """T = TypeVar("T")


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
    )


def class_and_init(name: str, methods: ContractMethods) -> DocumentParts:
    app_client_name = get_class_name(f"{name}Client")
    yield from indented(
        f"""
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
        )"""
    )
    yield Part.Gap1
    yield Part.IncIndent
    yield from call_methods(methods.no_op)
    yield Part.DecIndent


def embed_app_spec(app_spec: ApplicationSpecification) -> DocumentParts:
    yield Part.InlineMode
    yield 'APP_SPEC = """'
    yield app_spec.to_json()
    yield '"""'
    yield Part.RestoreLineMode


def call_method(method: Method) -> DocumentParts:
    yield f"def {get_method_name(method.name)}("
    yield Part.IncIndent
    yield "self,"
    yield "*,"
    for arg in method.args:
        yield f"{arg.name}: {map_abi_type_to_python(arg.type)},"
    yield "transaction_parameters: algokit_utils.TransactionParameters | None = None,"
    yield Part.DecIndent
    yield f") -> {map_abi_type_to_python(method.returns)}:"
    yield Part.IncIndent
    # TODO: yield doc
    args_class_name = get_class_name(f"{method.name}Args")
    if len(method.args) <= 3:
        yield Part.InlineMode
    yield f"args = {args_class_name}("
    if len(method.args) > 3:
        yield Part.IncIndent
    for arg in method.args:
        yield f"{arg.name}={arg.name},"
    if len(method.args) > 3:
        yield Part.DecIndent
    yield ")"
    if len(method.args) <= 3:
        yield Part.RestoreLineMode

    yield from indented(
        """
return self.app_client.call(
    call_abi_method=args.method(),
    transaction_parameters=convert(transaction_parameters),
    **as_dict(args),
)"""
    )
    yield Part.DecIndent


def call_methods(methods: list[Method | None]) -> DocumentParts:
    for method in methods:
        if method is None:
            pass
            # TODO: bare method
        else:
            yield from call_method(method)
        yield Part.Gap1


def generate(app_spec: ApplicationSpecification) -> DocumentParts:
    yield disable_linting()
    yield from imports()
    yield Part.Gap2
    methods = get_contract_methods(app_spec)
    yield from typed_arguments(methods)
    yield Part.Gap2
    yield from helpers()
    yield Part.Gap2
    yield from embed_app_spec(app_spec)
    yield Part.Gap2
    yield from class_and_init(app_spec.contract.name, methods)


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
        case Part.Gap1 | Part.Gap2:
            lines_needed = 2 if part == Part.Gap1 else 3  # need N + 1 lines
            trailing_lines = len(context.last_rendered_part) - len(context.last_rendered_part.rstrip("\n"))
            lines_to_add = lines_needed - trailing_lines
            if lines_to_add > 0:
                return "\n" * lines_to_add
            return None
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


# TODO: proper CLI arguments
input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])

app_spec = ApplicationSpecification.from_json(input_path.read_text())

output_path.write_text(render(generate(app_spec)))
