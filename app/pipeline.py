import os
import shutil
import stat

from app.analyzers.bandit_runner import run_bandit
from app.analyzers.ruff_runner import run_ruff
from app.repo_loader import clone_repo
from app.schemas import Finding
from app.ranking import rank_findings
from app.enricher import enrich_findings
from app.llm.gemini import GeminiClient


def _force_remove(func, path, _exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run_review(repo_url: str, use_llm: bool = True) -> list[Finding]:
    root = clone_repo(repo_url)
    try:
        findings = rank_findings(run_ruff(root) + run_bandit(root))
        if use_llm:
            findings = enrich_findings(root, findings, GeminiClient())
        return findings
    finally:
        shutil.rmtree(root, onerror=_force_remove)