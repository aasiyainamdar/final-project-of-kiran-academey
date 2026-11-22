from dao.application_dao import ApplicationDAO
from exception.custom_exceptions import (DuplicateRecordException, InvalidStatusTransitionException,
                                         RecordNotFoundException, ValidationException)
from service.candidate_service import CandidateService
from service.eligibility_service import EligibilityService
from service.job_service import JobService
from util.constants import ALLOWED_TRANSITIONS, APP_APPLIED, APP_SHORTLISTED, APP_REJECTED, CAND_VERIFIED
from util.db_connection import transaction
from util.logger import get_logger

log = get_logger(__name__)


class ApplicationService:
    def __init__(self):
        self.dao = ApplicationDAO()
        self.candidates = CandidateService()
        self.jobs = JobService()
        self.eligibility = EligibilityService()

    def apply_for_job(self, candidate_id, job_id):
        """Stage 3 - Application: verified candidate + open job + eligible + not a duplicate."""
        cand = self.candidates.get_candidate(candidate_id)
        job = self.jobs.get_job(job_id)
        if cand.status != CAND_VERIFIED:
            raise ValidationException(f"Candidate must be VERIFIED to apply (current: {cand.status}).")
        if self.dao.exists(candidate_id, job_id):                       # duplicate prevention (1)
            raise DuplicateRecordException("Candidate has already applied for this job.")
        self.eligibility.ensure_eligible(cand, job)                     # Eligibility Engine
        with transaction() as conn:
            app_id = self.dao.add_application(candidate_id, job_id, conn)   # UNIQUE key = prevention (2)
            self.dao.add_history(app_id, None, APP_APPLIED, conn)
        log.info("Application %s created (cand=%s job=%s)", app_id, candidate_id, job_id)
        return app_id

    def get_application(self, app_id, conn=None):
        row = self.dao.get_by_id(app_id, conn)
        if not row:
            raise RecordNotFoundException(f"Application {app_id} not found.")
        return row

    def change_status(self, app_id, new_status, conn=None):
        """Single gate for every workflow move; enforces ALLOWED_TRANSITIONS and logs history."""
        app = self.get_application(app_id, conn)
        old = app["status"]
        if new_status not in ALLOWED_TRANSITIONS.get(old, set()):
            raise InvalidStatusTransitionException(f"Cannot move application from {old} to {new_status}.")
        if conn is not None:
            self.dao.update_status(app_id, new_status, conn)
            self.dao.add_history(app_id, old, new_status, conn)
        else:
            with transaction() as c:
                self.dao.update_status(app_id, new_status, c)
                self.dao.add_history(app_id, old, new_status, c)
        log.info("Application %s: %s -> %s", app_id, old, new_status)

    def shortlist(self, app_id):
        """Stage 4 - Shortlisting."""
        self.change_status(app_id, APP_SHORTLISTED)

    def reject(self, app_id):
        self.change_status(app_id, APP_REJECTED)

    def withdraw(self, app_id):
        self.change_status(app_id, "WITHDRAWN")

    def list_applications(self, status=None):
        return self.dao.list_applications(status.upper() if status else None)

    def history(self, app_id):
        self.get_application(app_id)
        return self.dao.get_history(app_id)
