from dao.base_dao import BaseDAO


class CompanyDAO(BaseDAO):
    def add_company(self, c):
        return self.insert("INSERT INTO companies (name,location,industry,contact_email) VALUES (%s,%s,%s,%s)",
                           (c.name, c.location, c.industry, c.contact_email))

    def get_by_id(self, cid, conn=None):
        return self.fetch_one("SELECT * FROM companies WHERE company_id=%s", (cid,), conn)

    def list_all(self):
        return self.fetch_all("SELECT company_id,name,location,industry,contact_email,status "
                              "FROM companies ORDER BY company_id")

    def update_status(self, cid, status):
        return self.update("UPDATE companies SET status=%s WHERE company_id=%s", (status, cid))
