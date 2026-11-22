"""Candidate Eligibility Engine - checks every job requirement before a candidate may apply."""
from exception.custom_exceptions import NotEligibleException
from util.constants import QUALIFICATION_LEVEL, JOB_OPEN


class EligibilityService:
    def check(self, candidate, job):
        """Return a list of reasons why the candidate is NOT eligible (empty list = eligible)."""
        reasons = []
        if job.status != JOB_OPEN or job.vacancies <= 0:
            reasons.append("Job is closed / no vacancies")
        if QUALIFICATION_LEVEL[candidate.qualification] < QUALIFICATION_LEVEL[job.min_qualification]:
            reasons.append(f"Qualification {candidate.qualification} is below required {job.min_qualification}")
        if candidate.percentage < job.min_percentage:
            reasons.append(f"Percentage {candidate.percentage} is below required {job.min_percentage}")
        if not job.year_from <= candidate.passing_year <= job.year_to:
            reasons.append(f"Passing year {candidate.passing_year} not in {job.year_from}-{job.year_to}")
        if candidate.technology.lower() != job.technology.lower():
            reasons.append(f"Technology {candidate.technology} does not match {job.technology}")
        have = {s.lower() for s in candidate.skills}
        missing = [s for s in job.skills if s.lower() not in have]
        if missing:
            reasons.append("Missing skills: " + ", ".join(missing))
        if candidate.backlogs > job.max_backlogs:
            reasons.append(f"Backlogs {candidate.backlogs} exceed allowed {job.max_backlogs}")
        return reasons

    def ensure_eligible(self, candidate, job):
        reasons = self.check(candidate, job)
        if reasons:
            raise NotEligibleException(reasons)
        return True
