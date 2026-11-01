import ast
from dataclasses import dataclass, field
from pathlib import Path

from app.scanner import SourceFile


@dataclass
class FunctionInfo:
    name: str
    file: str
    start: int
    end: int
    calls: set[str] = field(default_factory=set)


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def index_file(root: Path, file: str) -> list[FunctionInfo]:
    try:
        path = (root / file).resolve()
        if not path.is_relative_to(root.resolve()):
            return []
        source = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source)
    except (OSError, SyntaxError):
        return []

    functions: list[FunctionInfo] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            calls = {
                name
                for child in ast.walk(node)
                if isinstance(child, ast.Call) and (name := _call_name(child))
            }
            functions.append(
                FunctionInfo(
                    name=node.name,
                    file=file,
                    start=node.lineno,
                    end=node.end_lineno or node.lineno,
                    calls=calls,
                )
            )
    return functions


def build_index(root: Path, files: list[SourceFile]) -> list[FunctionInfo]:
    index: list[FunctionInfo] = []
    for f in files:
        if f.language == "python":
            index.extend(index_file(root, f.path))
    return index
