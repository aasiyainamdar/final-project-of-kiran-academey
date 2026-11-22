"""Console menus. Every action is wrapped by @safe so custom exceptions print friendly messages."""
from datetime import datetime
from functools import wraps

from exception.custom_exceptions import NotEligibleException, RecruitmentException
from service.application_service import ApplicationService
from service.candidate_service import CandidateService
from service.company_service import CompanyService
from service.interview_service import InterviewService
from service.job_service import JobService
from service.offer_service import OfferService
from service.placement_service import PlacementService
from service.report_service import ReportService
from util.file_util import print_table
from util.logger import get_logger

log = get_logger(__name__)

candidate_service = CandidateService()
company_service = CompanyService()
job_service = JobService()
application_service = ApplicationService()
interview_service = InterviewService()
offer_service = OfferService()
placement_service = PlacementService()
report_service = ReportService()


def safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotEligibleException as e:
            print("\n  ✘ NOT ELIGIBLE:")
            for r in e.reasons:
                print("    -", r)
        except RecruitmentException as e:
            print(f"\n  ✘ {e}")
        except ValueError:
            print("\n  ✘ Invalid number / date format.")
        except Exception:
            log.exception("Unexpected error")
            print("\n  ✘ Unexpected error - see logs/app.log")
    return wrapper


def ask(label):
    return input(f"  {label}: ").strip()


def ask_int(label):
    return int(ask(label))


def run_menu(title, options):
    """options: list of (label, function). Loops until the user chooses Back."""
    while True:
        print(f"\n===== {title} =====")
        for i, (label, _) in enumerate(options, 1):
            print(f"  {i}. {label}")
        print("  0. Back")
        choice = ask("Enter your choice")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            options[int(choice) - 1][1]()
        else:
            print("  Invalid choice, try again.")


# ---------------- Candidate menu ----------------
@safe
def register_candidate():
    cid = candidate_service.register_candidate(
        ask("Candidate's full name"), ask("Email"), ask("Phone (10 digits)"),
        ask("Qualification (BE/BTECH/BSC/BCA/MCA...)"), ask("Percentage"), ask("Passing year"),
        ask("Main technology"), ask("Number of backlogs"),
        ask("Skills (comma separated)").split(","))
    print(f"\n  ✔ Candidate registered with ID {cid}")


@safe
def verify_candidate():
    candidate_service.verify_candidate(ask_int("Candidate ID to verify"))
    print("\n  ✔ Candidate verified")


@safe
def list_candidates():
    print_table(candidate_service.list_candidates())


@safe
def search_candidates():
    print_table(candidate_service.search_candidates(ask("Name/email contains"), ask("Technology (blank=any)"),
                                                    ask("Status (blank=any)")))


@safe
def update_phone():
    candidate_service.update_phone(ask_int("Candidate ID"), ask("New phone"))
    print("\n  ✔ Phone updated")


def candidate_menu():
    run_menu("CANDIDATE MANAGEMENT", [
        ("Add a new candidate", register_candidate), ("Verify candidate documents", verify_candidate),
        ("Show all candidates", list_candidates), ("Search / filter candidates", search_candidates),
        ("Update candidate phone", update_phone)])


# ---------------- Company & Job menu ----------------
@safe
def add_company():
    cid = company_service.add_company(ask("Company name"), ask("Location"), ask("Industry"), ask("Contact email"))
    print(f"\n  ✔ Company added with ID {cid}")


@safe
def list_companies():
    print_table(company_service.list_companies())


@safe
def post_job():
    jid = job_service.post_job(
        ask_int("Company ID"), ask("Job title"), ask("Technology"), ask("Minimum qualification"),
        ask("Minimum percentage"), ask("Passing year from"), ask("Passing year to"),
        ask("Maximum backlogs allowed"), ask("Vacancies"), ask("Salary (LPA)"),
        ask("Required skills (comma separated)").split(","))
    print(f"\n  ✔ Job posted with ID {jid}")


@safe
def deactivate_company():
    company_service.deactivate(ask_int("Company ID"))
    print("\n  ✔ Company deactivated")


@safe
def list_jobs():
    print_table(job_service.list_jobs(ask("Show only open jobs? (y/n)").lower() == "y"))


@safe
def close_job():
    job_service.close_job(ask_int("Job ID"))
    print("\n  ✔ Job closed")


def company_job_menu():
    run_menu("COMPANIES & JOBS", [
        ("Add company", add_company), ("View companies", list_companies), ("Publish a job opening", post_job),
        ("View jobs", list_jobs), ("Close a job", close_job),
        ("Deactivate company", deactivate_company)])


# ---------------- Application menu ----------------
@safe
def check_eligibility():
    cand = candidate_service.get_candidate(ask_int("Candidate ID"))
    job = job_service.get_job(ask_int("Job ID"))
    reasons = application_service.eligibility.check(cand, job)
    print("\n  ✔ Eligible" if not reasons else "\n  ✘ Not eligible:\n    - " + "\n    - ".join(reasons))


@safe
def apply_job():
    app_id = application_service.apply_for_job(ask_int("Candidate ID"), ask_int("Job ID"))
    print(f"\n  ✔ Application submitted with ID {app_id}")


@safe
def shortlist():
    application_service.shortlist(ask_int("Application ID"))
    print("\n  ✔ Application shortlisted")


@safe
def withdraw_application():
    application_service.withdraw(ask_int("Application ID"))
    print("\n  ✔ Application withdrawn")


@safe
def reject():
    application_service.reject(ask_int("Application ID"))
    print("\n  ✔ Application rejected")


@safe
def list_applications():
    print_table(application_service.list_applications(ask("Filter by status (blank=all)") or None))


@safe
def application_history():
    print_table(application_service.history(ask_int("Application ID")))


def application_menu():
    run_menu("APPLICATIONS", [
        ("Check eligibility", check_eligibility), ("Submit job application", apply_job),
        ("Shortlist candidate", shortlist), ("Reject application", reject), ("Withdraw application", withdraw_application),
        ("View applications", list_applications), ("View status history", application_history)])


# ---------------- Interview menu ----------------
@safe
def schedule_round():
    when = datetime.strptime(ask("Date & time (YYYY-MM-DD HH:MM)"), "%Y-%m-%d %H:%M")
    rid, no = interview_service.schedule_round(ask_int("Application ID"), ask("Round type (APTITUDE/TECHNICAL/MANAGERIAL/HR)"), when)
    print(f"\n  ✔ Round {no} scheduled (round id {rid})")


@safe
def give_feedback():
    interview_service.record_feedback(ask_int("Round ID"), ask("Rating (1-10)"), ask("Remarks"), ask("Result (PASS/FAIL)"))
    print("\n  ✔ Feedback saved")


@safe
def select_candidate():
    interview_service.select_candidate(ask_int("Application ID"))
    print("\n  ✔ Candidate selected")


@safe
def view_rounds():
    print_table(interview_service.rounds_of(ask_int("Application ID")))


def interview_menu():
    run_menu("INTERVIEWS", [
        ("Schedule next interview round", schedule_round), ("Record interview feedback", give_feedback),
        ("Select candidate", select_candidate), ("View rounds of an application", view_rounds)])


# ---------------- Offer & Placement menu ----------------
@safe
def generate_offer():
    app_id = ask_int("Application ID")
    sal = ask("Salary LPA (blank = job salary)")
    oid = offer_service.generate_offer(app_id, sal or None)
    print(f"\n  ✔ Offer generated with ID {oid}")


@safe
def respond_offer():
    offer_service.respond_to_offer(ask_int("Offer ID"), ask("Accept? (y/n)").lower() == "y")
    print("\n  ✔ Response recorded")


@safe
def list_offers():
    print_table(offer_service.list_offers())


@safe
def record_joining():
    pid = placement_service.record_joining(ask_int("Offer ID"), ask("Joining date (YYYY-MM-DD)"), ask("Joining location"))
    print(f"\n  ✔ Candidate placed! Placement ID {pid}")


@safe
def list_placements():
    print_table(placement_service.list_placements())


def offer_placement_menu():
    run_menu("OFFERS & PLACEMENTS", [
        ("Create offer letter", generate_offer), ("Record offer response", respond_offer),
        ("View offers", list_offers), ("Record joining & placement", record_joining),
        ("View placements", list_placements)])


# ---------------- Reports menu ----------------
def _report(name, getter):
    rows = getter()
    print_table(rows)
    if rows and ask("Export to CSV? (y/n)").lower() == "y":
        print("  Saved:", report_service.export(name, rows))


@safe
def overall_summary():
    print_table([report_service.summary()])


@safe
def company_report():
    _report("company_report", report_service.company_report)


@safe
def technology_report():
    _report("technology_report", report_service.technology_report)


@safe
def status_report():
    _report("application_status", report_service.application_status_report)


@safe
def popular_jobs():
    print_table(report_service.popular_jobs(int(ask("Minimum applications") or 2)))


@safe
def candidate_history():
    print_table(report_service.candidate_history(ask_int("Candidate ID")))


def report_menu():
    run_menu("MANAGEMENT REPORTS", [
        ("Placement dashboard summary", overall_summary), ("Company-wise placements", company_report),
        ("Technology-wise placements", technology_report), ("Application status summary", status_report),
        ("Jobs with many applications", popular_jobs), ("Candidate placement history", candidate_history)])
