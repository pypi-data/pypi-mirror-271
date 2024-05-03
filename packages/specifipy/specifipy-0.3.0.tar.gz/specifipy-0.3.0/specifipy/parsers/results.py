import dataclasses
from typing import Optional

from specifipy.parsers.structure.code_structure_definitions import (
    ClassStructureDefinition,
    Docstring,
    FieldStructureDefinition,
    FunctionStructureDefinition,
)


@dataclasses.dataclass
class ParsingResult:
    classes: list[ClassStructureDefinition]
    functions: list[FunctionStructureDefinition]
    class_fields: list[FieldStructureDefinition]
    docstrings: Optional[list[Docstring]] = None
