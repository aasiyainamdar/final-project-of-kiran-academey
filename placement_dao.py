from dao.base_dao import BaseDAO


class PlacementDAO(BaseDAO):
    def add_joining(self, offer_id, joining_date, location, conn=None):
        return self.insert("INSERT INTO joining_details (offer_id,joining_date,location) VALUES (%s,%s,%s)",
                           (offer_id, joining_date, location), conn)

    def add_placement(self, p, conn=None):
        return self.insert("INSERT INTO placements (candidate_id,company_id,job_id,offer_id,salary_lpa,placed_on) "
                           "VALUES (%s,%s,%s,%s,%s,%s)",
                           (p.candidate_id, p.company_id, p.job_id, p.offer_id, p.salary_lpa, p.placed_on), conn)

    def list_placements(self):
        return self.fetch_all("SELECT p.placement_id, ca.name AS candidate, co.name AS company, j.title AS job, "
                              "p.salary_lpa, p.placed_on FROM placements p "
                              "JOIN candidates ca ON ca.candidate_id=p.candidate_id "
                              "JOIN companies co ON co.company_id=p.company_id "
                              "JOIN jobs j ON j.job_id=p.job_id ORDER BY p.placement_id")
