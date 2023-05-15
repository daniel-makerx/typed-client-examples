from collections.abc import Iterable, Sequence
from enum import Enum


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


AtomicDocumentPart = str | Part
DocumentPart = AtomicDocumentPart | Sequence[AtomicDocumentPart]
DocumentParts = Iterable[DocumentPart]


class RenderContext:
    def __init__(self, *, indent_inc: str):
        self.line_mode_stack = ["\n"]
        self.indent_inc = indent_inc

        self.last_part: DocumentPart | None = None
        self.indent = ""
        self.last_rendered_part = ""

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
            if context.last_part in [Part.Gap1, Part.Gap2]:  # collapse gaps
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


def convert_part(part: DocumentPart, context: RenderContext) -> list[str]:
    parts: Sequence[AtomicDocumentPart]
    match part:
        case str() | Part():
            parts = [part]
        case _:
            parts = part
    results = []
    for part in parts:
        result = convert_part_inner(part, context)
        context.last_part = part
        if result is not None:
            if len(result) > 5:
                context.last_rendered_part = result
            else:  # if last render was small then combine
                context.last_rendered_part += result
            results.append(result)
    return results
