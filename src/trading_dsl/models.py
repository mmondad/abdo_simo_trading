"""Machine-readable validation report models."""

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class Status(StrEnum):
    EXTRACTED = "EXTRACTED"
    VALIDATED = "VALIDATED"
    UNRESOLVED = "UNRESOLVED"
    UNSUPPORTED_FEATURE = "UNSUPPORTED_FEATURE"
    UNSUPPORTED_PATTERN = "UNSUPPORTED_PATTERN"
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"
    EXECUTABLE = "EXECUTABLE"
    BACKTESTED = "BACKTESTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class Issue:
    layer: str
    code: str
    path: str
    message: str
    category: str | None = None
    missing_feature: str | None = None
    source_reference: dict[str, Any] | None = None
    suggested_action: str | None = None


@dataclass
class ValidationReport:
    paper_id: str | None
    strategy_id: str | None
    status: Status
    issues: list[Issue] = field(default_factory=list)
    registry_versions: dict[str, str] = field(default_factory=dict)

    @property
    def valid(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def grouped_capabilities(self) -> list[dict[str, Any]]:
        groups: dict[tuple[str | None, str | None], list[str]] = {}
        for issue in self.issues:
            if issue.layer == "capability":
                groups.setdefault((issue.category, issue.missing_feature), []).append(issue.path)
        return [
            {"issue_category": k[0], "missing_feature": k[1], "paths": sorted(v), "count": len(v)}
            for k, v in sorted(groups.items(), key=lambda item: str(item[0]))
        ]
