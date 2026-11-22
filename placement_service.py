from datetime import date

from dao.candidate_dao import CandidateDAO
from dao.job_dao import JobDAO
from dao.offer_dao import OfferDAO
from dao.placement_dao import PlacementDAO
from exception.custom_exceptions import InvalidStatusTransitionException, RecordNotFoundException
from model.placement import Placement
from service.application_service import ApplicationService
from util.constants import APP_JOINED, APP_PLACED, CAND_PLACED, JOB_CLOSED, OFFER_ACCEPTED
from util.db_connection import transaction
from util.logger import get_logger

log = get_logger(__name__)


class PlacementService:
    def __init__(self):
        self.dao = PlacementDAO()
        self.offer_dao = OfferDAO()
        self.cand_dao = CandidateDAO()
        self.job_dao = JobDAO()
        self.apps = ApplicationService()

    def record_joining(self, offer_id, joining_date, location):
        """Stages 9 & 10 - Joining -> Placement, done as ONE atomic transaction."""
        offer = self.offer_dao.get_by_id(offer_id)
        if not offer:
            raise RecordNotFoundException(f"Offer {offer_id} not found.")
        if offer["status"] != OFFER_ACCEPTED:
            raise InvalidStatusTransitionException("Only ACCEPTED offers can be converted to joining.")
        app = self.apps.get_application(offer["application_id"])
        job = self.job_dao.get_by_id(app["job_id"])
        with transaction() as conn:
            self.dao.add_joining(offer_id, joining_date, location, conn)
            self.apps.change_status(app["application_id"], APP_JOINED, conn)
            self.apps.change_status(app["application_id"], APP_PLACED, conn)
            self.cand_dao.update_status(app["candidate_id"], CAND_PLACED, conn)
            placement = Placement(app["candidate_id"], job["company_id"], job["job_id"], offer_id,
                                  float(offer["salary_lpa"]), date.today())
            pid = self.dao.add_placement(placement, conn)
            self.job_dao.reduce_vacancy(job["job_id"], conn)
            if job["vacancies"] - 1 <= 0:
                self.job_dao.update_status(job["job_id"], JOB_CLOSED, conn)
        log.info("Placement %s recorded for candidate %s", pid, app["candidate_id"])
        return pid

    def list_placements(self):
        return self.dao.list_placements()
