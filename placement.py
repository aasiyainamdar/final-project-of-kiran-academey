from dataclasses import dataclass
from datetime import date


@dataclass
class Placement:
    candidate_id: int
    company_id: int
    job_id: int
    offer_id: int
    salary_lpa: float
    placed_on: date
    placement_id: int = None

    @classmethod
    def from_row(cls, r):
        return cls(r["candidate_id"], r["company_id"], r["job_id"], r["offer_id"],
                   float(r["salary_lpa"]), r["placed_on"], r["placement_id"])
