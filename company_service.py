from dao.company_dao import CompanyDAO
from exception.custom_exceptions import RecordNotFoundException
from model.company import Company
from util import validators as v
from util.logger import get_logger

log = get_logger(__name__)


class CompanyService:
    def __init__(self):
        self.dao = CompanyDAO()

    def add_company(self, name, location, industry, email):
        company = Company(v.validate_name(name), v.validate_name(location), industry.strip(),
                          v.validate_email(email) if email else "")
        cid = self.dao.add_company(company)
        log.info("Company added id=%s name=%s", cid, name)
        return cid

    def get_company(self, cid):
        row = self.dao.get_by_id(cid)
        if not row:
            raise RecordNotFoundException(f"Company {cid} not found.")
        return Company.from_row(row)

    def list_companies(self):
        return self.dao.list_all()

    def deactivate(self, cid):
        self.get_company(cid)
        self.dao.update_status(cid, "INACTIVE")
