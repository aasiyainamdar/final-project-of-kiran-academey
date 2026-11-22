from dao.base_dao import BaseDAO


class CandidateDAO(BaseDAO):
    def add_candidate(self, c, conn=None):
        sql = """INSERT INTO candidates (name,email,phone,qualification,percentage,passing_year,
                 technology,backlogs,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cid = self.insert(sql, (c.name, c.email, c.phone, c.qualification, c.percentage,
                                c.passing_year, c.technology, c.backlogs, c.status), conn)
        for skill in c.skills:
            self.insert("INSERT INTO candidate_skills (candidate_id, skill) VALUES (%s,%s)", (cid, skill), conn)
        return cid

    def get_by_id(self, cid, conn=None):
        return self.fetch_one("SELECT * FROM candidates WHERE candidate_id=%s", (cid,), conn)

    def get_skills(self, cid, conn=None):
        rows = self.fetch_all("SELECT skill FROM candidate_skills WHERE candidate_id=%s", (cid,), conn)
        return [r["skill"] for r in rows]

    def list_all(self):
        return self.fetch_all("SELECT candidate_id,name,email,qualification,percentage,passing_year,"
                              "technology,backlogs,status FROM candidates ORDER BY candidate_id")

    def search(self, keyword="", technology="", status=""):
        sql = ("SELECT candidate_id,name,email,qualification,percentage,technology,status "
               "FROM candidates WHERE (name LIKE %s OR email LIKE %s)")
        params = [f"%{keyword}%", f"%{keyword}%"]
        if technology:
            sql += " AND technology=%s"
            params.append(technology)
        if status:
            sql += " AND status=%s"
            params.append(status)
        return self.fetch_all(sql + " ORDER BY name", tuple(params))

    def update_status(self, cid, status, conn=None):
        return self.update("UPDATE candidates SET status=%s WHERE candidate_id=%s", (status, cid), conn)

    def update_contact(self, cid, phone):
        return self.update("UPDATE candidates SET phone=%s WHERE candidate_id=%s", (phone, cid))
