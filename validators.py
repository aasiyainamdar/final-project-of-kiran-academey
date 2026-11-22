"""Input validation helpers. All raise ValidationException on bad data."""
import re
from datetime import date

from exception.custom_exceptions import ValidationException
from util.constants import QUALIFICATION_LEVEL

_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
_PHONE = re.compile(r"^[6-9]\d{9}$")


def validate_name(name):
    if not name or len(name.strip()) < 2:
        raise ValidationException("Name must have at least 2 characters.")
    return name.strip()


def validate_email(email):
    if not email or not _EMAIL.match(email.strip()):
        raise ValidationException("Invalid email address.")
    return email.strip().lower()


def validate_phone(phone):
    if not phone or not _PHONE.match(phone.strip()):
        raise ValidationException("Phone must be 10 digits starting with 6-9.")
    return phone.strip()


def validate_percentage(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValidationException("Percentage must be a number.")
    if not 0 <= value <= 100:
        raise ValidationException("Percentage must be between 0 and 100.")
    return value


def validate_year(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationException("Passing year must be a number.")
    if not 1990 <= value <= date.today().year + 1:
        raise ValidationException("Passing year is out of range.")
    return value


def validate_qualification(q):
    q = (q or "").strip().upper()
    if q not in QUALIFICATION_LEVEL:
        raise ValidationException(
            "Unknown qualification. Use one of: " + ", ".join(sorted(QUALIFICATION_LEVEL)))
    return q


def validate_positive_number(value, label="Value"):
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValidationException(f"{label} must be a number.")
    if value <= 0:
        raise ValidationException(f"{label} must be greater than zero.")
    return value


def validate_non_negative_int(value, label="Value"):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationException(f"{label} must be a whole number.")
    if value < 0:
        raise ValidationException(f"{label} cannot be negative.")
    return value
