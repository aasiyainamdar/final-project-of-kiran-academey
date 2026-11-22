from dataclasses import dataclass


@dataclass
class Company:
    name: str
    location: str
    industry: str = ""
    contact_email: str = ""
    status: str = "ACTIVE"
    company_id: int = None

    @classmethod
    def from_row(cls, r):
        return cls(r["name"], r["location"], r["industry"], r["contact_email"], r["status"], r["company_id"])
