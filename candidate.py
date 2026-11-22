from dataclasses import dataclass, field
from typing import List


@dataclass
class Candidate:
    name: str
    email: str
    phone: str
    qualification: str
    percentage: float
    passing_year: int
    technology: str
    backlogs: int = 0
    skills: List[str] = field(default_factory=list)
    status: str = "REGISTERED"
    candidate_id: int = None

    @classmethod
    def from_row(cls, row, skills=None):
        return cls(row["name"], row["email"], row["phone"], row["qualification"],
                   float(row["percentage"]), row["passing_year"], row["technology"],
                   row["backlogs"], skills or [], row["status"], row["candidate_id"])
