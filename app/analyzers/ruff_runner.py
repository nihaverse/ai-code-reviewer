import json
import os
import subprocess
import sys
from pathlib import Path

from app.schemas import Finding


def _classify(code: str) -> tuple[str, str]:
    """Map a Ruff rule code to (category, severity)."""
    if code.startswith(("F", "B")):
        return "bug", "medium"
    return "style", "low"


def run_ruff(root: Path) -> list[Finding]:
    result = subprocess.run(
        [
            sys.executable, "-m", "ruff", "check",
            "--isolated", "--no-cache",
            "--select", "F,B,E,W",
            "--output-format", "json",
            str(root),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    findings: list[Finding] = []
    for item in json.loads(result.stdout or "[]"):
        category, severity = _classify(item["code"])
        findings.append(
            Finding(
                file=Path(os.path.relpath(item["filename"], root)).as_posix(),
                line=item["location"]["row"],
                category=category,
                severity=severity,
                rule_id=item["code"],
                message=item["message"],
                source="ruff",
            )
        )
    return findings