from dataclasses import dataclass
from typing import Dict, List


@dataclass(kw_only=True)
class Selected:
    """
    Struct for obj that matched the schema
    """

    idx: int
    item: Dict


@dataclass(kw_only=True)
class Rejected:
    """
    Struct for obj that didn't match the schema
    """

    idx: int
    item: Dict
    reasons: List[str]

    def __repr__(self) -> str:
        return f"Filtered Item: [{self.idx}]\n\t" + "\n\t".join(self.reasons)


@dataclass(kw_only=True)
class FilterResult:
    """
    Struct for the result
    """

    selected: List[Selected]
    rejected: List[Rejected]

    @property
    def total_selected(self) -> int:
        return len(self.selected)

    @property
    def total_rejected(self) -> int:
        return len(self.rejected)

    def __repr__(self) -> str:
        return f"Total Selected: {len(self.selected)}\n" + "\n".join(
            [str(rejects) for rejects in self.rejected]
        )
