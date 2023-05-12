import dataclasses
import re
import sys
from collections.abc import Callable, Iterable
from enum import Enum
from pathlib import Path
from typing import Literal

from algosdk.abi import ABIType, Method, Returns

from algokit_utils import ApplicationSpecification, CallConfig, MethodConfigDict, MethodHints, OnCompleteActionName


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
ESCAPED_QUOTE = r"\""
SINGLE_QUOTE = '"'
TRIPLE_QUOTE = '"""'


@dataclasses.dataclass(kw_only=True)
class ContractArg:
    name: str
    abi_type: str
    python_type: str
    desc: str
    has_default: bool = False


@dataclasses.dataclass(kw_only=True)
class ContractMethod:
    abi_method: Method | None
    on_complete: OnCompleteActionName
    call_config: Literal["call", "create"]
    abi_type: str | None = None
    python_type: str | None = None
    args: list[ContractArg] = dataclasses.field(default_factory=list)
    hints: MethodHints | None = None
    args_class_name: str | None = None
    client_method_name: str | None = None

    @property
    def is_bare(self) -> bool:
        return self.abi_method is None


@dataclasses.dataclass(kw_only=True)
class ContractMethods:
    no_op: list[ContractMethod] = dataclasses.field(default_factory=list)
    create: list[ContractMethod] = dataclasses.field(default_factory=list)
    update_application: list[ContractMethod] = dataclasses.field(default_factory=list)
    delete_application: list[ContractMethod] = dataclasses.field(default_factory=list)
    opt_in: list[ContractMethod] = dataclasses.field(default_factory=list)
    close_out: list[ContractMethod] = dataclasses.field(default_factory=list)

    @property
    def all_methods(self) -> Iterable[ContractMethod]:
        yield from self.no_op
        yield from self.create
        yield from self.update_application
        yield from self.delete_application
        yield from self.opt_in
        yield from self.close_out

    def has_abi_methods(self) -> bool:
        return any(m for m in self.all_methods if not m.is_bare)

    def add_method(
        self, app_spec: ApplicationSpecification, method: Method | None, method_config: MethodConfigDict
    ) -> None:
        if method and method.args:
            hints = app_spec.hints[method.get_signature()]
            args = [
                ContractArg(
                    name=arg.name,
                    abi_type=arg.type,
                    python_type=map_abi_type_to_python(arg.type),
                    desc=arg.desc,
                    has_default=arg.name in hints.default_arguments,
                )
                for arg in method.args
            ]
        else:
            hints = None
            args = []
        for on_complete, call_config in method_config.items():
            if call_config & CallConfig.CALL != CallConfig.NEVER:
                collection = getattr(self, on_complete)
                contract_method = ContractMethod(
                    abi_method=method, call_config="call", on_complete=on_complete, args=args, hints=hints
                )
                collection.append(contract_method)
            if call_config & CallConfig.CREATE != CallConfig.NEVER:
                contract_method = ContractMethod(
                    abi_method=method, call_config="create", on_complete=on_complete, args=args, hints=hints
                )
                self.create.append(contract_method)


@dataclasses.dataclass(kw_only=True)
class GenerateContext:
    app_spec: ApplicationSpecification
    methods: ContractMethods = dataclasses.field(init=False)
    used_module_symbols: set[str] = dataclasses.field(default_factory=set)
    used_client_symbols: set[str] = dataclasses.field(default_factory=set)
    disable_linting: bool = True


def get_contract_methods(context: GenerateContext) -> ContractMethods:
    result = ContractMethods()
    app_spec = context.app_spec
    result.add_method(app_spec, None, app_spec.bare_call_config)

    for method in app_spec.contract.methods:
        hints = app_spec.hints[method.get_signature()]
        result.add_method(app_spec, method, hints.call_config)

    return result


def get_parts(value: str) -> list[str]:
    """Splits value into a list of words, with boundaries at _, and transitions between casing"""
    return re.findall("[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]", value)


def get_class_name(name: str, string_suffix: str = "") -> str:
    parts = [p.title() for p in get_parts(name)]
    if string_suffix:
        parts.append(string_suffix)
    return "".join(p for p in parts)


def get_method_name(name: str, string_suffix: str = "") -> str:
    parts = [p.lower() for p in get_parts(name)]
    if string_suffix:
        parts.append(string_suffix)
    return "_".join(p for p in parts)


def lines(block: str) -> DocumentParts:
    yield from block.splitlines()


def disable_linting(context: GenerateContext) -> str:
    return "# flake8: noqa"  # this works for flake8 and ruff


def imports(context: GenerateContext) -> DocumentParts:
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
    yield TRIPLE_QUOTE
    value_lines = value.splitlines()
    last_idx = len(value_lines) - 1
    for idx, line in enumerate(value_lines):
        if idx == 0 and line.startswith(SINGLE_QUOTE):
            quotes_at_start = len(line) - len(line.lstrip(SINGLE_QUOTE))
            yield ESCAPED_QUOTE * quotes_at_start
            line = line[quotes_at_start:]
        if idx == last_idx and line.endswith(SINGLE_QUOTE) and not line.endswith(ESCAPED_QUOTE):
            yield line[:-1].replace(TRIPLE_QUOTE, ESCAPED_QUOTE)
            yield ESCAPED_QUOTE
        else:
            yield line.replace(TRIPLE_QUOTE, ESCAPED_QUOTE)
        if idx != last_idx:
            yield Part.NewLine
    yield TRIPLE_QUOTE
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


def typed_argument_class(contract_method: ContractMethod) -> DocumentParts:
    method = contract_method.abi_method
    args_class_name = contract_method.args_class_name
    return_type = map_abi_type_to_python(method.returns)
    yield "@dataclasses.dataclass(kw_only=True)"
    yield f"class {args_class_name}(_ArgsBase[{return_type}]):"
    yield Part.IncIndent
    if method.desc:
        yield from docstring(method.desc)
    for arg in contract_method.args:
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
    yield string_literal(method.get_signature())
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
    for method in context.methods.no_op:
        if method is None:
            continue
        yield from typed_argument_class(method)
        yield Part.Gap2
    # TODO: additional ABI types


def helpers(context: GenerateContext) -> DocumentParts:
    yield '_T = TypeVar("_T")'
    if context.methods.has_abi_methods():
        yield '_TReturn = TypeVar("_TReturn")'
        yield Part.Gap2
        yield from indented(
            """
class _ArgsBase(ABC, Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ..."""
        )
    yield Part.Gap2
    yield from indented(
        """
def _as_dict(data: _T | None) -> dict[str, Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


def _convert(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.CommonCallParametersDict | None:
    if transaction_parameters is None:
        return None
    return cast(algokit_utils.CommonCallParametersDict, _as_dict(transaction_parameters))


def _convert_create(
    transaction_parameters: algokit_utils.CreateTransactionParameters | None,
) -> algokit_utils.CreateCallParametersDict | None:
    if transaction_parameters is None:
        return None
    return cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))"""
    )


def class_and_init(context: GenerateContext) -> DocumentParts:
    app_client_name = get_class_name(f"{context.app_spec.contract.name}Client")
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
    yield Part.DecIndent


def embed_app_spec(context: GenerateContext) -> DocumentParts:
    yield Part.InlineMode
    yield 'APP_SPEC = """'
    yield context.app_spec.to_json()
    yield '"""'
    yield Part.RestoreLineMode


def call_method(context: GenerateContext, contract_method: ContractMethod) -> DocumentParts:
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

    # TODO: better control over when to inline
    args = contract_method.args
    declaration = f"args = {contract_method.args_class_name}("
    arg_length = sum(len(a.name) * 2 + 2 for a in args) + len(declaration) + 1
    if arg_length < 76:
        yield Part.InlineMode
        yield declaration
        for arg in args:
            yield f"{arg.name}={arg.name},"
        yield ")"
        yield Part.RestoreLineMode
    else:
        yield declaration
        yield Part.IncIndent
        for arg in contract_method.args:
            yield f"{arg.name}={arg.name},"
        yield Part.DecIndent
        yield ")"

    yield from indented(
        """
return self.app_client.call(
    call_abi_method=args.method(),
    transaction_parameters=_convert(transaction_parameters),
    **_as_dict(args),
)"""
    )
    yield Part.DecIndent


def call_methods(context: GenerateContext) -> DocumentParts:
    for method in context.methods.no_op:
        if method.is_bare:
            yield from indented(
                """
def no_op(self) -> algokit_utils.TransactionResponse:
    return self.app_client.call(
        call_abi_method=False,
        transaction_parameters=_convert(transaction_parameters),
    )"""
            )
        else:
            yield from call_method(context, method)
        yield Part.Gap1


def _get_unique_symbol_by_incrementing(
    existing_symbols: set[str], base_name: str, factory: Callable[[str, str], str]
) -> str:
    suffix = 0
    while True:
        suffix_str = str(suffix) if suffix else ""
        symbol = factory(base_name, suffix_str)
        if symbol not in existing_symbols:
            existing_symbols.add(symbol)
            return symbol


def create_generate_context(app_spec: ApplicationSpecification) -> GenerateContext:
    context = GenerateContext(app_spec=app_spec)
    context.used_module_symbols.update(
        "APP_SPEC", "_T", "_TResult", "_ArgsBase", "_as_dict", "_convert", "_convert_create"
    )
    context.used_client_symbols.update(
        "__init__",
        "app_spec",
        "app_client",
        "no_op",
        "create",
        "update",
        "delete",
        "opt_in",
        "close_out",
        "clear",
        "deploy",
    )
    context.client_name = _get_unique_symbol_by_incrementing(
        context.used_module_symbols, f"{app_spec.contract.name}_client", get_class_name
    )
    context.methods = get_contract_methods(context)
    for method in context.methods.all_methods:
        if method.is_bare:
            continue
        method_name = method.abi_method.name
        method.args_class_name = _get_unique_symbol_by_incrementing(
            context.used_module_symbols, f"{method_name}_args", get_class_name
        )
        method.client_method_name = _get_unique_symbol_by_incrementing(
            context.used_client_symbols, method_name, get_method_name
        )

    return context


def generate(context: GenerateContext) -> DocumentParts:
    if context.disable_linting:
        yield disable_linting(context)
    yield from imports(context)
    yield Part.Gap1
    yield from embed_app_spec(context)
    yield from helpers(context)
    yield Part.Gap2
    yield from typed_arguments(context)
    yield Part.Gap2
    yield from class_and_init(context)


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
            if context.last_rendered_part in [Part.Gap1, Part.Gap2]:  # collapse gaps
                return None
            lines_needed = int(part.name[3:]) + 1  # N + 1
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
        if len(result) > 5:
            context.last_rendered_part = result
        else:  # if last render was small then combine
            context.last_rendered_part += result
    return result


def render(parts: DocumentParts, indent_size: int = 4) -> str:
    context = RenderContext(line_mode_stack=["\n"], indent="", indent_inc=" " * indent_size, last_part=None)

    rendered_parts = [convert_part(p, context) for p in parts]
    return "".join(p for p in rendered_parts if p is not None)


def main():
    # TODO: proper CLI parsing
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    app_spec = ApplicationSpecification.from_json(input_path.read_text())

    context = create_generate_context(app_spec)
    output = render(generate(context))
    output_path.write_text(output)


if __name__ == "__main__":
    main()
