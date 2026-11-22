from dataclasses import dataclass


@dataclass
class Application:
    candidate_id: int
    job_id: int
    status: str = "APPLIED"
    application_id: int = None

    @classmethod
    def from_row(cls, r):
        return cls(r["candidate_id"], r["job_id"], r["status"], r["application_id"])
