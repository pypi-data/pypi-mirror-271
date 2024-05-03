import abc
import ast
from enum import Enum

import javalang.parse
from javalang.tree import CompilationUnit, FieldDeclaration, MethodDeclaration

from specifipy.parsers.results import ParsingResult
from specifipy.parsers.structure.code_structure_definitions import (
    ClassStructureDefinition,
    Docstring,
    FunctionStructureDefinition,
    NotTypeAnnotatedFieldStructureDefinition,
    StructureEnum,
    TypeAnnotatedFieldStructureDefinition,
)


class FileType(Enum):
    PYTHON = "python"
    JAVA = "java"


class GenericParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, source_code_file_content: str) -> ParsingResult:
        pass


class ParserFactory:
    @staticmethod
    def get_parser(file_type: FileType) -> GenericParser:
        if file_type == FileType.PYTHON:
            return PythonParser()
        if file_type == FileType.JAVA:
            return JavaParser()
        raise NotImplementedError(f"Unsupported file type: {file_type}")


class JavaParser(GenericParser):
    def __generate_method_definition(
        self, method: MethodDeclaration, parent_class: ClassStructureDefinition
    ) -> FunctionStructureDefinition:
        name: str = method.name
        return_type: str = None
        if "private" in method.modifiers:
            name = f"-{name}"

        params: list[str] = []
        if method.parameters:
            for param in method.parameters:
                params.append(
                    f"{param.type.name} {'<' + param.arguments[0].name + '>' if (hasattr(param, 'arguments') and param.arguments) else ''} {param.name}"
                )
        if method.return_type:
            return_type = method.return_type.name
        return FunctionStructureDefinition(
            StructureEnum.FUNCTION,
            name,
            method.position.line,
            method.position.line,
            params,
            parent_class,
            return_type,
        )

    def parse(self, source_code_file_content: str) -> ParsingResult:
        tree: CompilationUnit = javalang.parse.parse(source_code_file_content)
        parsing_result: ParsingResult = ParsingResult([], [], [])

        if (
            tree.types
        ):  # This list represents classes defined in the Java file. Should be 1 per file.
            for declaration in tree.types:
                class_structure = ClassStructureDefinition(
                    StructureEnum.CLASS,
                    declaration.name,
                    declaration.position.line,
                    declaration.position.line,
                    declaration.extends.name if declaration.extends else None,
                    [interface.name for interface in declaration.implements]
                    if hasattr(declaration, "implements") and declaration.implements
                    else None,
                )
                parsing_result.classes.append(class_structure)
                # Extract documentation if present
                if declaration.documentation:
                    docstring = Docstring(declaration.documentation)
                    if parsing_result.docstrings is not None:
                        parsing_result.docstrings.append(docstring)
                    else:
                        parsing_result.docstrings = [docstring]

                # Now methods
                if (
                    declaration.methods
                ):  # might be None if no method is declared (various DTOs etc.)
                    methods: list[FunctionStructureDefinition] = []
                    for method in declaration.methods:
                        methods.append(
                            self.__generate_method_definition(method, class_structure)
                        )
                    parsing_result.functions = methods

                # And fields
                if declaration.fields:
                    field: FieldDeclaration
                    for field in declaration.fields:
                        name: str = (
                            field.declarators[0].name
                            if not "private" in field.modifiers
                            else f"-{field.declarators[0].name}"
                        )
                        field_type: str = field.type.name
                        field_structure = TypeAnnotatedFieldStructureDefinition(
                            StructureEnum.CLASS_FIELD,
                            name,
                            field.position.line,
                            field.position.line,
                            class_structure,
                            field_type,
                        )
                        parsing_result.class_fields.append(field_structure)
        return parsing_result


class PythonParser(GenericParser):
    def __init__(self):
        pass

    def get_return_type_annotation(self, function_node: ast.FunctionDef) -> str | None:
        # Check if the function has a return type annotation directly
        if function_node.returns:
            return ast.unparse(function_node.returns)

        # If not, try to find the return type annotation in the function body
        for node in ast.walk(function_node):
            if isinstance(node, ast.Return):
                if (
                    isinstance(node.value, ast.NameConstant)
                    and node.value.value is None
                ):
                    continue
                if isinstance(node.value, ast.AnnAssign):
                    return ast.unparse(node.value.annotation)
        return None

    def __classify_node(
        self, node: ast.AST, parsing_result: ParsingResult, parent=None
    ) -> None:
        match type(node):
            case ast.ClassDef:
                node: ast.ClassDef
                name: str = node.name
                inherits_from = ""
                if len(node.bases) > 0:
                    if isinstance(node.bases[0], ast.Name):
                        inherits_from = node.bases[0].id
                    if isinstance(node.bases[0], ast.Attribute):
                        inherits_from = f"{node.bases[0].value.id if hasattr(node.bases[0].value, 'id') else node.bases[0].value.value.id}_{node.bases[0].attr}"

                class_definition = ClassStructureDefinition(
                    StructureEnum.CLASS,
                    name,
                    node.lineno,
                    node.end_lineno,
                    inherits_from,
                )

                if class_definition not in parsing_result.classes:
                    parsing_result.classes.append(class_definition)
                sub_node: ast.AST
                for sub_node in node.body:
                    self.__classify_node(
                        sub_node, parsing_result, parent=class_definition
                    )

            case ast.FunctionDef:
                node: ast.FunctionDef
                name: str = node.name
                params: ast.arguments = node.args
                params_string: list[str] = [x.arg for x in params.args]
                function_definition = FunctionStructureDefinition(
                    StructureEnum.FUNCTION,
                    name,
                    node.lineno,
                    node.end_lineno,
                    params_string,
                    (parent if parent else None),
                    str(self.get_return_type_annotation(node)),
                )
                if function_definition not in parsing_result.functions:
                    parsing_result.functions.append(function_definition)

            case ast.AnnAssign:
                if isinstance(parent, ClassStructureDefinition) and parent:
                    node: ast.AnnAssign
                    name: str = node.target.id
                    type_annotation: str = (
                        node.annotation.id
                        if not isinstance(
                            node.annotation,
                            (ast.Attribute, ast.Subscript, ast.BinOp, ast.Call),
                        )
                        else node.annotation.attr
                        if isinstance(node.annotation, ast.Attribute)
                        else ast.unparse(node.annotation.slice)
                        if isinstance(node.annotation, ast.Subscript)
                        else ast.unparse(node.annotation)
                        if isinstance(node.annotation, ast.BinOp)
                        else ast.unparse(node.annotation)
                    )
                    field = TypeAnnotatedFieldStructureDefinition(
                        StructureEnum.CLASS_FIELD,
                        name,
                        node.lineno,
                        node.end_lineno,
                        parent,
                        type_annotation,
                    )
                    parsing_result.class_fields.append(field)

            case ast.Assign:
                if isinstance(parent, ClassStructureDefinition) and parent:
                    node: ast.Assign
                    name: str = (
                        node.targets[0].id
                        if isinstance(node.targets[0], ast.Name)
                        else node.targets[0].attr
                        if isinstance(node.targets[0], ast.Attribute)
                        else str(node.targets[0])
                    )
                    field = NotTypeAnnotatedFieldStructureDefinition(
                        StructureEnum.CLASS_FIELD,
                        name,
                        node.lineno,
                        node.end_lineno,
                        parent,
                    )
                    parsing_result.class_fields.append(field)

    def parse(self, source_code_file_content: str) -> ParsingResult:
        code = ast.parse(source_code_file_content)
        parsing_result: ParsingResult = ParsingResult([], [], [])
        for node in ast.walk(code):
            self.__classify_node(node, parsing_result)
        return parsing_result
