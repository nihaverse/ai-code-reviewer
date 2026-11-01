import shutil
import subprocess
import tempfile
from pathlib import Path


def clone_repo(repo_url: str) -> Path:
    """Shallow-clone a repo into a temp folder and return its path."""
    target = Path(tempfile.mkdtemp(prefix="review_"))
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(target)],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        raise
    return target