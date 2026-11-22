from dao.job_dao import JobDAO
from exception.custom_exceptions import RecordNotFoundException, ValidationException
from model.job import Job
from service.company_service import CompanyService
from util import validators as v
from util.constants import JOB_CLOSED
from util.logger import get_logger

log = get_logger(__name__)


class JobService:
    def __init__(self):
        self.dao = JobDAO()
        self.company_service = CompanyService()

    def post_job(self, company_id, title, technology, min_qualification, min_percentage,
                 year_from, year_to, max_backlogs, vacancies, salary_lpa, skills):
        company = self.company_service.get_company(company_id)
        if company.status != "ACTIVE":
            raise ValidationException("Cannot post a job for an inactive company.")
        y_from, y_to = v.validate_year(year_from), v.validate_year(year_to)
        if y_from > y_to:
            raise ValidationException("'Passing year from' cannot be after 'passing year to'.")
        job = Job(company_id, v.validate_name(title), v.validate_name(technology).title(),
                  v.validate_qualification(min_qualification), v.validate_percentage(min_percentage),
                  y_from, y_to, v.validate_non_negative_int(max_backlogs, "Max backlogs"),
                  int(v.validate_positive_number(vacancies, "Vacancies")),
                  v.validate_positive_number(salary_lpa, "Salary"),
                  sorted({s.strip().title() for s in skills if s.strip()}))
        jid = self.dao.add_job(job)
        log.info("Job posted id=%s title=%s", jid, job.title)
        return jid

    def get_job(self, jid):
        row = self.dao.get_by_id(jid)
        if not row:
            raise RecordNotFoundException(f"Job {jid} not found.")
        return Job.from_row(row, self.dao.get_skills(jid))

    def list_jobs(self, only_open=False):
        return self.dao.list_jobs("OPEN" if only_open else None)

    def close_job(self, jid):
        self.get_job(jid)
        self.dao.update_status(jid, JOB_CLOSED)
        log.info("Job %s closed", jid)
