"""Reporting queries: joins, GROUP BY, HAVING and aggregate functions."""
from dao.base_dao import BaseDAO


class ReportDAO(BaseDAO):
    def placements_by_company(self):
        return self.fetch_all("SELECT co.name AS company, COUNT(p.placement_id) AS placed, "
                              "ROUND(AVG(p.salary_lpa),2) AS avg_salary_lpa, MAX(p.salary_lpa) AS max_salary_lpa "
                              "FROM companies co LEFT JOIN placements p ON p.company_id=co.company_id "
                              "GROUP BY co.company_id, co.name ORDER BY placed DESC")

    def placements_by_technology(self):
        return self.fetch_all("SELECT ca.technology, COUNT(*) AS placed, ROUND(AVG(p.salary_lpa),2) AS avg_salary_lpa "
                              "FROM placements p JOIN candidates ca ON ca.candidate_id=p.candidate_id "
                              "GROUP BY ca.technology ORDER BY placed DESC")

    def application_status_summary(self):
        return self.fetch_all("SELECT status, COUNT(*) AS total FROM applications GROUP BY status ORDER BY total DESC")

    def candidate_status_summary(self):
        return self.fetch_all("SELECT status, COUNT(*) AS total FROM candidates GROUP BY status")

    def jobs_with_many_applications(self, minimum=2):
        return self.fetch_all("SELECT j.job_id, j.title, COUNT(a.application_id) AS applications FROM jobs j "
                              "JOIN applications a ON a.job_id=j.job_id GROUP BY j.job_id, j.title "
                              "HAVING COUNT(a.application_id) >= %s ORDER BY applications DESC", (minimum,))

    def candidate_placement_history(self, candidate_id):
        return self.fetch_all("SELECT a.application_id, j.title AS job, co.name AS company, a.status, "
                              "DATE(a.applied_on) AS applied_on FROM applications a "
                              "JOIN jobs j ON j.job_id=a.job_id JOIN companies co ON co.company_id=j.company_id "
                              "WHERE a.candidate_id=%s ORDER BY a.applied_on", (candidate_id,))

    def overall_summary(self):
        return self.fetch_one("SELECT (SELECT COUNT(*) FROM candidates) AS candidates, "
                              "(SELECT COUNT(*) FROM companies) AS companies, "
                              "(SELECT COUNT(*) FROM jobs WHERE status='OPEN') AS open_jobs, "
                              "(SELECT COUNT(*) FROM applications) AS applications, "
                              "(SELECT COUNT(*) FROM placements) AS placements")
