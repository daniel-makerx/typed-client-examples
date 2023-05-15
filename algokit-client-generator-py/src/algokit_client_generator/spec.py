import dataclasses
import typing
from collections.abc import Iterable

from algokit_utils import ApplicationSpecification, CallConfig, MethodConfigDict, MethodHints, OnCompleteActionName
from algosdk.abi import Method

from algokit_client_generator import utils


@dataclasses.dataclass(kw_only=True)
class ContractArg:
    name: str
    abi_type: str
    python_type: str
    desc: str | None
    has_default: bool = False


@dataclasses.dataclass(kw_only=True)
class ABIContractMethod:
    method: Method
    hints: MethodHints
    abi_type: str
    python_type: str
    args: list[ContractArg] = dataclasses.field(default_factory=list)
    args_class_name: str | None = None
    client_method_name: str | None = None


@dataclasses.dataclass(kw_only=True)
class ContractMethod:
    abi: ABIContractMethod | None
    on_complete: list[OnCompleteActionName]
    call_config: typing.Literal["call", "create"]


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

    @property
    def all_abi_methods(self) -> Iterable[ContractMethod]:
        return (m for m in self.all_methods if m.abi)

    @property
    def has_abi_methods(self) -> bool:
        return any(self.all_abi_methods)

    def add_method(
        self, app_spec: ApplicationSpecification, method: Method | None, method_config: MethodConfigDict
    ) -> None:
        if method:
            hints = app_spec.hints[method.get_signature()]
            abi = ABIContractMethod(
                method=method,
                hints=hints,
                abi_type=str(method.returns),
                python_type=utils.map_abi_type_to_python(str(method.returns)),
                args=[
                    ContractArg(
                        name=arg.name or f"arg{idx}",
                        abi_type=str(arg.type),
                        python_type=utils.map_abi_type_to_python(str(arg.type)),
                        desc=arg.desc,
                        has_default=arg.name in hints.default_arguments,
                    )
                    for idx, arg in enumerate(method.args)
                ],
            )
        else:
            abi = None

        create_on_completes = []
        for on_complete, call_config in method_config.items():
            if call_config & CallConfig.CALL != CallConfig.NEVER:
                collection = getattr(self, on_complete)
                contract_method = ContractMethod(
                    abi=abi,
                    call_config="call",
                    on_complete=[on_complete],
                )
                collection.append(contract_method)
            if call_config & CallConfig.CREATE != CallConfig.NEVER:
                create_on_completes.append(on_complete)

        if create_on_completes:
            contract_method = ContractMethod(
                abi=abi,
                call_config="create",
                on_complete=create_on_completes,
            )
            self.create.append(contract_method)


def get_contract_methods(app_spec: ApplicationSpecification) -> ContractMethods:
    result = ContractMethods()
    result.add_method(app_spec, None, app_spec.bare_call_config)

    for method in app_spec.contract.methods:
        hints = app_spec.hints[method.get_signature()]
        result.add_method(app_spec, method, hints.call_config)

    return result
