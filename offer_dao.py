from dao.base_dao import BaseDAO


class OfferDAO(BaseDAO):
    def add_offer(self, app_id, salary, offer_date, conn=None):
        return self.insert("INSERT INTO offers (application_id,salary_lpa,offer_date) VALUES (%s,%s,%s)",
                           (app_id, salary, offer_date), conn)

    def get_by_id(self, offer_id, conn=None):
        return self.fetch_one("SELECT * FROM offers WHERE offer_id=%s", (offer_id,), conn)

    def update_status(self, offer_id, status, conn=None):
        return self.update("UPDATE offers SET status=%s WHERE offer_id=%s", (status, offer_id), conn)

    def list_offers(self):
        return self.fetch_all("SELECT o.offer_id, ca.name AS candidate, co.name AS company, j.title AS job, "
                              "o.salary_lpa, o.offer_date, o.status FROM offers o "
                              "JOIN applications a ON a.application_id=o.application_id "
                              "JOIN candidates ca ON ca.candidate_id=a.candidate_id "
                              "JOIN jobs j ON j.job_id=a.job_id JOIN companies co ON co.company_id=j.company_id "
                              "ORDER BY o.offer_id")
