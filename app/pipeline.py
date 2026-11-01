import os
import shutil
import stat

from app.analyzers.bandit_runner import run_bandit
from app.analyzers.ruff_runner import run_ruff
from app.repo_loader import clone_repo
from app.schemas import Finding


def _force_remove(func, path, _exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run_review(repo_url: str) -> list[Finding]:
    root = clone_repo(repo_url)
    try:
        return run_ruff(root) + run_bandit(root)
    finally:
        shutil.rmtree(root, onerror=_force_remove)