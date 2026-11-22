from dao.candidate_dao import CandidateDAO
from exception.custom_exceptions import RecordNotFoundException, InvalidStatusTransitionException, ValidationException
from model.candidate import Candidate
from util import validators as v
from util.constants import CAND_REGISTERED, CAND_VERIFIED
from util.logger import get_logger

log = get_logger(__name__)


class CandidateService:
    def __init__(self):
        self.dao = CandidateDAO()

    def register_candidate(self, name, email, phone, qualification, percentage, passing_year,
                           technology, backlogs, skills):
        """Stage 1 - Candidate Registration (validates every field, then inserts)."""
        if v.validate_percentage(percentage) < 35:
            raise ValidationException("Candidates with less than 35% cannot be registered.")
        cand = Candidate(
            name=v.validate_name(name), email=v.validate_email(email), phone=v.validate_phone(phone),
            qualification=v.validate_qualification(qualification),
            percentage=v.validate_percentage(percentage), passing_year=v.validate_year(passing_year),
            technology=v.validate_name(technology).title(),
            backlogs=v.validate_non_negative_int(backlogs, "Backlogs"),
            skills=sorted({s.strip().title() for s in skills if s.strip()}), status=CAND_REGISTERED)
        cid = self.dao.add_candidate(cand)          # raises DuplicateRecordException for same email
        log.info("Candidate registered id=%s email=%s", cid, cand.email)
        return cid

    def get_candidate(self, cid):
        row = self.dao.get_by_id(cid)
        if not row:
            raise RecordNotFoundException(f"Candidate {cid} not found.")
        return Candidate.from_row(row, self.dao.get_skills(cid))

    def verify_candidate(self, cid):
        """Stage 2 - Eligibility Verification (documents verified by the placement officer)."""
        cand = self.get_candidate(cid)
        if cand.status != CAND_REGISTERED:
            raise InvalidStatusTransitionException(f"Candidate is already {cand.status}.")
        self.dao.update_status(cid, CAND_VERIFIED)
        log.info("Candidate %s verified", cid)

    def update_phone(self, cid, phone):
        self.get_candidate(cid)
        self.dao.update_contact(cid, v.validate_phone(phone))

    def list_candidates(self):
        return self.dao.list_all()

    def search_candidates(self, keyword="", technology="", status=""):
        return self.dao.search(keyword.strip(), technology.strip().title(), status.strip().upper())
