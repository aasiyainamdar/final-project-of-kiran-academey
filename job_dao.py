from dao.base_dao import BaseDAO


class JobDAO(BaseDAO):
    def add_job(self, j):
        sql = """INSERT INTO jobs (company_id,title,technology,min_qualification,min_percentage,year_from,
                 year_to,max_backlogs,vacancies,salary_lpa,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        jid = self.insert(sql, (j.company_id, j.title, j.technology, j.min_qualification, j.min_percentage,
                                j.year_from, j.year_to, j.max_backlogs, j.vacancies, j.salary_lpa, j.status))
        for s in j.skills:
            self.insert("INSERT INTO job_skills (job_id,skill) VALUES (%s,%s)", (jid, s))
        return jid

    def get_by_id(self, jid, conn=None):
        return self.fetch_one("SELECT * FROM jobs WHERE job_id=%s", (jid,), conn)

    def get_skills(self, jid, conn=None):
        return [r["skill"] for r in self.fetch_all("SELECT skill FROM job_skills WHERE job_id=%s", (jid,), conn)]

    def list_jobs(self, status=None):
        sql = ("SELECT j.job_id, c.name AS company, j.title, j.technology, j.min_qualification AS qualification, "
               "j.min_percentage AS min_pct, j.vacancies, j.salary_lpa, j.status "
               "FROM jobs j JOIN companies c ON c.company_id=j.company_id")
        if status:
            return self.fetch_all(sql + " WHERE j.status=%s ORDER BY j.job_id", (status,))
        return self.fetch_all(sql + " ORDER BY j.job_id")

    def update_status(self, jid, status, conn=None):
        return self.update("UPDATE jobs SET status=%s WHERE job_id=%s", (status, jid), conn)

    def reduce_vacancy(self, jid, conn=None):
        return self.update("UPDATE jobs SET vacancies=vacancies-1 WHERE job_id=%s AND vacancies>0", (jid,), conn)
