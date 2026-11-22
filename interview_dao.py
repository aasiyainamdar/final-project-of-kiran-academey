from dao.base_dao import BaseDAO


class InterviewDAO(BaseDAO):
    def next_round_no(self, app_id, conn=None):
        row = self.fetch_one("SELECT COALESCE(MAX(round_no),0)+1 AS n FROM interview_rounds WHERE application_id=%s",
                             (app_id,), conn)
        return row["n"]

    def add_round(self, app_id, round_no, round_type, scheduled_on, conn=None):
        return self.insert("INSERT INTO interview_rounds (application_id,round_no,round_type,scheduled_on) "
                           "VALUES (%s,%s,%s,%s)", (app_id, round_no, round_type, scheduled_on), conn)

    def get_round(self, round_id, conn=None):
        return self.fetch_one("SELECT * FROM interview_rounds WHERE round_id=%s", (round_id,), conn)

    def pending_rounds(self, app_id, conn=None):
        return self.fetch_all("SELECT * FROM interview_rounds WHERE application_id=%s AND status='SCHEDULED'",
                              (app_id,), conn)

    def mark_completed(self, round_id, conn=None):
        return self.update("UPDATE interview_rounds SET status='COMPLETED' WHERE round_id=%s", (round_id,), conn)

    def add_feedback(self, round_id, rating, remarks, result, conn=None):
        return self.insert("INSERT INTO interview_feedback (round_id,rating,remarks,result) VALUES (%s,%s,%s,%s)",
                           (round_id, rating, remarks, result), conn)

    def count_passed(self, app_id, conn=None):
        row = self.fetch_one("SELECT COUNT(*) AS n FROM interview_feedback f JOIN interview_rounds r "
                             "ON r.round_id=f.round_id WHERE r.application_id=%s AND f.result='PASS'",
                             (app_id,), conn)
        return row["n"]

    def rounds_for_application(self, app_id):
        return self.fetch_all("SELECT r.round_id, r.round_no, r.round_type, r.scheduled_on, r.status, "
                              "f.rating, f.result, f.remarks FROM interview_rounds r "
                              "LEFT JOIN interview_feedback f ON f.round_id=r.round_id "
                              "WHERE r.application_id=%s ORDER BY r.round_no", (app_id,))
