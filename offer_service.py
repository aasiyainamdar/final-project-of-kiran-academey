from datetime import date

from dao.offer_dao import OfferDAO
from exception.custom_exceptions import InvalidStatusTransitionException, RecordNotFoundException, ValidationException
from service.application_service import ApplicationService
from util.constants import APP_OFFERED, APP_REJECTED, APP_SELECTED, OFFER_ACCEPTED, OFFER_PENDING, OFFER_REJECTED
from util.db_connection import transaction
from util.logger import get_logger

log = get_logger(__name__)


class OfferService:
    def __init__(self):
        self.dao = OfferDAO()
        self.apps = ApplicationService()

    def generate_offer(self, app_id, salary_lpa=None):
        """Stage 8 - Offer. Defaults to the salary advertised on the job."""
        app = self.apps.get_application(app_id)
        if app["status"] != APP_SELECTED:
            raise InvalidStatusTransitionException(f"Only SELECTED candidates get offers (current: {app['status']}).")
        job = self.apps.jobs.get_job(app["job_id"])
        salary = float(salary_lpa) if salary_lpa else job.salary_lpa
        if salary <= 0:
            raise ValidationException("Salary must be greater than zero.")
        if salary < job.salary_lpa * 0.5:
            raise ValidationException(f"Offer salary cannot be below 50% of the job salary ({job.salary_lpa} LPA).")
        with transaction() as conn:
            offer_id = self.dao.add_offer(app_id, salary, date.today(), conn)
            self.apps.change_status(app_id, APP_OFFERED, conn)
        log.info("Offer %s generated for application %s", offer_id, app_id)
        return offer_id

    def respond_to_offer(self, offer_id, accept):
        offer = self.dao.get_by_id(offer_id)
        if not offer:
            raise RecordNotFoundException(f"Offer {offer_id} not found.")
        if offer["status"] != OFFER_PENDING:
            raise InvalidStatusTransitionException(f"Offer is already {offer['status']}.")
        with transaction() as conn:
            if accept:
                self.dao.update_status(offer_id, OFFER_ACCEPTED, conn)
            else:
                self.dao.update_status(offer_id, OFFER_REJECTED, conn)
                self.apps.change_status(offer["application_id"], APP_REJECTED, conn)

    def list_offers(self):
        return self.dao.list_offers()
