from dataclasses import dataclass
from datetime import date


@dataclass
class Offer:
    application_id: int
    salary_lpa: float
    offer_date: date
    status: str = "PENDING"
    offer_id: int = None

    @classmethod
    def from_row(cls, r):
        return cls(r["application_id"], float(r["salary_lpa"]), r["offer_date"], r["status"], r["offer_id"])
