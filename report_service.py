from dao.report_dao import ReportDAO
from util.file_util import export_to_csv


class ReportService:
    def __init__(self):
        self.dao = ReportDAO()

    def summary(self):
        return self.dao.overall_summary()

    def company_report(self):
        return self.dao.placements_by_company()

    def technology_report(self):
        return self.dao.placements_by_technology()

    def application_status_report(self):
        return self.dao.application_status_summary()

    def popular_jobs(self, minimum=2):
        return self.dao.jobs_with_many_applications(minimum)

    def candidate_history(self, candidate_id):
        return self.dao.candidate_placement_history(candidate_id)

    def export(self, name, rows):
        return export_to_csv(rows, name)
