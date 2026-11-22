from dao.interview_dao import InterviewDAO
from exception.custom_exceptions import InvalidStatusTransitionException, RecordNotFoundException, ValidationException
from service.application_service import ApplicationService
from util.constants import (MAX_INTERVIEW_ROUNDS, APP_INTERVIEW, APP_REJECTED, APP_SELECTED, APP_SHORTLISTED, ROUND_TYPES,
                            RESULT_FAIL, RESULT_PASS)
from util.db_connection import transaction
from util.logger import get_logger

log = get_logger(__name__)


class InterviewService:
    def __init__(self):
        self.dao = InterviewDAO()
        self.apps = ApplicationService()

    def schedule_round(self, app_id, round_type, scheduled_on):
        """Stage 5 - Interview Scheduling (round numbers are tracked automatically)."""
        round_type = round_type.strip().upper()
        if round_type not in ROUND_TYPES:
            raise ValidationException("Round type must be one of: " + ", ".join(ROUND_TYPES))
        app = self.apps.get_application(app_id)
        if app["status"] not in (APP_SHORTLISTED, APP_INTERVIEW):
            raise InvalidStatusTransitionException(
                f"Only SHORTLISTED / in-interview applications can be scheduled (current: {app['status']}).")
        if self.dao.pending_rounds(app_id):
            raise InvalidStatusTransitionException("Previous round is still pending - give its feedback first.")
        if len(self.dao.rounds_for_application(app_id)) >= MAX_INTERVIEW_ROUNDS:
            raise ValidationException(f"Maximum {MAX_INTERVIEW_ROUNDS} interview rounds allowed per application.")
        with transaction() as conn:
            round_no = self.dao.next_round_no(app_id, conn)
            rid = self.dao.add_round(app_id, round_no, round_type, scheduled_on, conn)
            self.apps.change_status(app_id, APP_INTERVIEW, conn)
        log.info("Round %s (%s) scheduled for application %s", round_no, round_type, app_id)
        return rid, round_no

    def record_feedback(self, round_id, rating, remarks, result):
        """Stage 6 - Interview Feedback. A FAIL result rejects the application automatically."""
        result = result.strip().upper()
        if result not in (RESULT_PASS, RESULT_FAIL):
            raise ValidationException("Result must be PASS or FAIL.")
        try:
            rating = int(rating)
        except ValueError:
            raise ValidationException("Rating must be a number 1-10.")
        if not 1 <= rating <= 10:
            raise ValidationException("Rating must be between 1 and 10.")
        rnd = self.dao.get_round(round_id)
        if not rnd:
            raise RecordNotFoundException(f"Interview round {round_id} not found.")
        if rnd["status"] != "SCHEDULED":
            raise InvalidStatusTransitionException("Feedback was already given for this round.")
        with transaction() as conn:
            self.dao.add_feedback(round_id, rating, remarks.strip(), result, conn)
            self.dao.mark_completed(round_id, conn)
            if result == RESULT_FAIL:
                self.apps.change_status(rnd["application_id"], APP_REJECTED, conn)
        log.info("Feedback saved for round %s result=%s", round_id, result)

    def select_candidate(self, app_id):
        """Stage 7 - Selection (needs >=1 passed round and no pending round)."""
        app = self.apps.get_application(app_id)
        if app["status"] != APP_INTERVIEW:
            raise InvalidStatusTransitionException(f"Application is {app['status']}, not in interview stage.")
        if self.dao.pending_rounds(app_id):
            raise InvalidStatusTransitionException("A round is still pending.")
        if self.dao.count_passed(app_id) < 1:
            raise InvalidStatusTransitionException("Candidate has not passed any interview round.")
        self.apps.change_status(app_id, APP_SELECTED)

    def rounds_of(self, app_id):
        self.apps.get_application(app_id)
        return self.dao.rounds_for_application(app_id)
