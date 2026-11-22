from dataclasses import dataclass
from datetime import datetime


@dataclass
class InterviewRound:
    application_id: int
    round_no: int
    round_type: str
    scheduled_on: datetime
    status: str = "SCHEDULED"
    round_id: int = None

    @classmethod
    def from_row(cls, r):
        return cls(r["application_id"], r["round_no"], r["round_type"], r["scheduled_on"],
                   r["status"], r["round_id"])
