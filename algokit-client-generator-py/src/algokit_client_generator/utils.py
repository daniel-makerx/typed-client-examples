import re


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


def map_abi_type_to_python(abi_type: str) -> str:
    match = re.match(r".*\[([0-9]*)]$", abi_type)
    if match:
        array_size = match.group(1)
        if array_size:
            abi_type = abi_type[: -2 - len(array_size)]
            array_size = int(array_size)
            inner_type = ", ".join([map_abi_type_to_python(abi_type)] * array_size)
            return f"tuple[{inner_type}]"
        else:
            abi_type = abi_type[:-2]
            if abi_type == "byte":
                return "bytes"
            return f"list[{map_abi_type_to_python(abi_type)}]"
    if abi_type.startswith("(") and abi_type.endswith(")"):
        abi_type = abi_type[1:-1]
        inner_types = [map_abi_type_to_python(t) for t in abi_type.split(",")]
        return f"tuple[{', '.join(inner_types)}]"
    # TODO validate or annotate ints
    python_type = {
        "string": "str",
        "uint8": "int",  # < 256
        "uint32": "int",  # < 2^32
        "uint64": "int",  # < 2^64
        "void": "None",
        "byte[]": "bytes",
        "byte": "bytes",  # length 1
        "pay": "TransactionWithSigner",
    }.get(abi_type)
    if python_type:
        return python_type
    return abi_type