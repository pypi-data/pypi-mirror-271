import dataclasses
from enum import Enum


class StructureEnum(Enum):
    CLASS = 1
    FUNCTION = 2
    VARIABLE = 3
    CLASS_FIELD = 4


class ParamDefinition:
    name: str
    type: str


@dataclasses.dataclass
class Docstring:
    content: str


@dataclasses.dataclass
class StructureDefinition:
    structure_type: StructureEnum
    name: str
    start_line: int
    end_line: int

    # This is not a comprehensive list
    d2_reserved_keywords = [
        "label",
        "class",
        "classes",
        "style",
        "shape",
        "direction",
        "width",
        "height",
        "link",
    ]

    # This hack is to avoid failure on diagram generation when a D2 keyword is encountered
    def sanitize_d2_names(self):
        keyword_escape_char: str = "⠀"
        if self.name.lower() in self.d2_reserved_keywords:
            self.name = self.name + keyword_escape_char

    def __post_init__(self):
        self.sanitize_d2_names()


@dataclasses.dataclass
class ClassStructureDefinition(StructureDefinition):
    inherits_from: str
    implements: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class FunctionStructureDefinition(StructureDefinition):
    params: list[str]
    parent_class: ClassStructureDefinition
    return_type: str = None

    def __eq__(self, other):
        return (
            self.name,
            self.params,
            self.start_line,
            self.end_line,
            self.structure_type,
        ) == (
            other.name,
            other.params,
            other.start_line,
            other.end_line,
            other.structure_type,
        )


@dataclasses.dataclass
class FieldStructureDefinition(StructureDefinition):
    parent_class: ClassStructureDefinition


@dataclasses.dataclass
class TypeAnnotatedFieldStructureDefinition(FieldStructureDefinition):
    type_annotation: str


@dataclasses.dataclass
class NotTypeAnnotatedFieldStructureDefinition(FieldStructureDefinition):
    pass
