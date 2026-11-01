from app.schemas import Finding

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
CATEGORY_ORDER = {"security": 0, "bug": 1, "style": 2}

# Bandit import/subprocess warnings: too generic to be useful on their own
NOISE_RULES = {"B403", "B404", "B603", "B607"}


def rank_findings(findings: list[Finding]) -> list[Finding]:
    best: dict[tuple, Finding] = {}
    for f in findings:
        if f.rule_id in NOISE_RULES:
            continue
        key = (f.file, f.line, f.category)
        current = best.get(key)
        if current is None or SEVERITY_ORDER[f.severity] < SEVERITY_ORDER[current.severity]:
            best[key] = f
    return sorted(
        best.values(),
        key=lambda f: (SEVERITY_ORDER[f.severity], CATEGORY_ORDER[f.category], f.file, f.line),
    )