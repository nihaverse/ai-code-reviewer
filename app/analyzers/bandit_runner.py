import json
import os
import subprocess
import sys
from pathlib import Path

from app.schemas import Finding


def run_bandit(root: Path) -> list[Finding]:
    result = subprocess.run(
        [sys.executable, "-m", "bandit", "-r", str(root), "-f", "json", "-q"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    findings: list[Finding] = []
    for item in json.loads(result.stdout or "{}").get("results", []):
        findings.append(
            Finding(
                file=Path(os.path.relpath(item["filename"], root)).as_posix(),
                line=item["line_number"],
                category="security",
                severity=item["issue_severity"].lower(),
                rule_id=item["test_id"],
                message=item["issue_text"],
                source="bandit",
            )
        )
    return findings