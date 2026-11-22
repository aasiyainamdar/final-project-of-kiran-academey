from dataclasses import dataclass, field
from typing import List


@dataclass
class Job:
    company_id: int
    title: str
    technology: str
    min_qualification: str
    min_percentage: float
    year_from: int
    year_to: int
    max_backlogs: int
    vacancies: int
    salary_lpa: float
    skills: List[str] = field(default_factory=list)
    status: str = "OPEN"
    job_id: int = None

    @classmethod
    def from_row(cls, r, skills=None):
        return cls(r["company_id"], r["title"], r["technology"], r["min_qualification"],
                   float(r["min_percentage"]), r["year_from"], r["year_to"], r["max_backlogs"],
                   r["vacancies"], float(r["salary_lpa"]), skills or [], r["status"], r["job_id"])
