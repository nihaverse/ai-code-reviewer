import os
from dataclasses import dataclass
from pathlib import Path

IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".idea", ".vscode", ".tox",
}

LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go",
}

MAX_FILE_SIZE = 200_000  # bytes


@dataclass
class SourceFile:
    path: str  # relative to the repo root
    language: str
    size: int


def scan_repo(root: Path) -> list[SourceFile]:
    """Walk a repo and return the source files worth reviewing."""
    files: list[SourceFile] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            full = Path(dirpath) / name
            language = LANGUAGES.get(full.suffix.lower())
            if language is None:
                continue
            size = full.stat().st_size
            if size > MAX_FILE_SIZE:
                continue
            files.append(
                SourceFile(
                    path=full.relative_to(root).as_posix(),
                    language=language,
                    size=size,
                )
            )
    return files