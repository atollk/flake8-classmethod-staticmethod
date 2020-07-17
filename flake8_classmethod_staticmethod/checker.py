import argparse
import ast
import sys
from typing import Iterable, Tuple

import flake8.options.manager

DEFAULT_SELECT = [
    "CLST101",
    "CLST131",
]

PYTHON_38 = sys.version_info >= (3, 8)


class Checker:
    """
    flake8 plugin that checks rules regarding the staticmethod and classmethod decorators.
    """

    name = "flake8-classmethod-staticmethod"
    version = "1.0"
    enabled_errors = []

    def __init__(self, tree: ast.AST):
        self.tree = tree

    @staticmethod
    def add_options(option_manager: flake8.options.manager.OptionManager):
        option_manager.add_option(
            "--select_clst1",
            type=str,
            comma_separated_list=True,
            default=DEFAULT_SELECT,
            parse_from_config=True,
            help="Error types to use. Default: %(default)s",
        )

    @classmethod
    def parse_options(
        cls,
        option_manager: flake8.options.manager.OptionManager,
        options: argparse.Namespace,
        extra_args,
    ):
        cls.enabled_errors = [
            int(option[4:]) for option in options.select_clst1
        ]

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        for cls_node in ast.walk(self.tree):
            if isinstance(cls_node, ast.ClassDef):
                classname = cls_node.name
                for fn_node in ast.walk(cls_node):
                    if isinstance(fn_node, ast.FunctionDef):
                        yield from self._check_function_node(fn_node, classname)

    def _check_function_node(self, fn_node: ast.FunctionDef, classname: str):
        is_staticmethod = any(
            isinstance(deco, ast.Name) and deco.id == "staticmethod"
            for deco in fn_node.decorator_list
        )
        is_classmethod = any(
            isinstance(deco, ast.Name) and deco.id == "classmethod"
            for deco in fn_node.decorator_list
        )
        if is_staticmethod:
            if 100 in self.enabled_errors:
                yield from _clst100(fn_node)
            if 101 in self.enabled_errors:
                yield from _clst101(fn_node, classname)
        if is_classmethod:
            if 130 in self.enabled_errors:
                yield from _clst130(fn_node)
            if 131 in self.enabled_errors:
                yield from _clst131(fn_node)
            if 132 in self.enabled_errors:
                yield from _clst132(fn_node, classname)


ERROR_MESSAGES = {
    100: "@staticmethod is used. (hint: try @classmethod or a normal method instead)",
    101: "@staticmethod references its containing class. (hint: use @classmethod instead)",
    130: "@classmethod is used. (hint: try @staticmethod or a normal method instead)",
    131: "@classmethod does not use the cls parameter. (hint: use @staticmethod instead)",
    132: "@classmethod references its containing class by name. (hint: use the first parameter instead)",
}


def _function_uses_identifier(node: ast.FunctionDef, identifier: str) -> bool:
    return any(
        isinstance(child, ast.Name) and child.id == identifier
        for child in ast.walk(node)
    )


def _error_tuple(error_code: int, node: ast.AST) -> Tuple[int, int, str, type]:
    return (
        node.lineno,
        node.col_offset,
        f"CLST{error_code} {ERROR_MESSAGES[error_code]}",
        Checker,
    )


def _clst100(node: ast.FunctionDef) -> Iterable[Tuple[int, int, str, type]]:
    yield _error_tuple(100, node)


def _clst101(
    node: ast.FunctionDef, classname: str
) -> Iterable[Tuple[int, int, str, type]]:
    references_class = any(
        isinstance(child, ast.Name) and child.id == classname
        for child in ast.walk(node)
    )
    if references_class:
        yield _error_tuple(101, node)


def _clst130(node: ast.FunctionDef) -> Iterable[Tuple[int, int, str, type]]:
    yield _error_tuple(130, node)


def _clst131(node: ast.FunctionDef) -> Iterable[Tuple[int, int, str, type]]:
    if node.args.args:
        cls_param = node.args.args[0].arg
        if not _function_uses_identifier(node, cls_param):
            yield _error_tuple(131, node)


def _clst132(
    node: ast.FunctionDef, classname: str
) -> Iterable[Tuple[int, int, str, type]]:
    if _function_uses_identifier(node, classname):
        yield _error_tuple(132, node)
