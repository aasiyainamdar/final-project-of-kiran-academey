"""Application entry point.  Run from the project root:  python -m app.main"""
from app.menu import (application_menu, candidate_menu, company_job_menu, interview_menu,
                      offer_placement_menu, report_menu, run_menu)
from util.db_connection import get_connection
from exception.custom_exceptions import DatabaseException
from util.logger import get_logger

log = get_logger(__name__)


def main():
    print("=" * 56)
    print("   RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM")
    print("=" * 56)
    try:
        get_connection().close()
    except DatabaseException as e:
        print(f"\n  ✘ {e}\n  Check config/db_config.py and make sure MySQL is running.")
        return
    log.info("Application started")
    run_menu("RECRUITMENT & PLACEMENT HOME", [
        ("Candidate Management", candidate_menu), ("Companies & Jobs", company_job_menu),
        ("Applications & Eligibility", application_menu), ("Interviews", interview_menu),
        ("Offers & Placements", offer_placement_menu), ("Management Reports", report_menu)])
    log.info("Application closed")
    print("\n  Thank you for using the system. Goodbye!")


if __name__ == "__main__":
    main()
