from dao.base_dao import BaseDAO


class ApplicationDAO(BaseDAO):
    def exists(self, candidate_id, job_id, conn=None):
        row = self.fetch_one("SELECT application_id FROM applications WHERE candidate_id=%s AND job_id=%s",
                             (candidate_id, job_id), conn)
        return row is not None

    def add_application(self, candidate_id, job_id, conn=None):
        return self.insert("INSERT INTO applications (candidate_id,job_id,status) VALUES (%s,%s,'APPLIED')",
                           (candidate_id, job_id), conn)

    def get_by_id(self, app_id, conn=None):
        return self.fetch_one("SELECT * FROM applications WHERE application_id=%s", (app_id,), conn)

    def update_status(self, app_id, status, conn=None):
        return self.update("UPDATE applications SET status=%s WHERE application_id=%s", (status, app_id), conn)

    def add_history(self, app_id, old, new, conn=None):
        return self.insert("INSERT INTO application_status_history (application_id,old_status,new_status) "
                           "VALUES (%s,%s,%s)", (app_id, old, new), conn)

    def get_history(self, app_id):
        return self.fetch_all("SELECT old_status,new_status,changed_on FROM application_status_history "
                              "WHERE application_id=%s ORDER BY history_id", (app_id,))

    def list_applications(self, status=None):
        sql = ("SELECT a.application_id, ca.name AS candidate, j.title AS job, co.name AS company, "
               "a.status, DATE(a.applied_on) AS applied_on FROM applications a "
               "JOIN candidates ca ON ca.candidate_id=a.candidate_id "
               "JOIN jobs j ON j.job_id=a.job_id JOIN companies co ON co.company_id=j.company_id")
        if status:
            return self.fetch_all(sql + " WHERE a.status=%s ORDER BY a.application_id", (status,))
        return self.fetch_all(sql + " ORDER BY a.application_id")
