
import re
from datetime import datetime, date


def validate_patient(full_name, dob, email,
                     glucose, haemoglobin, cholesterol):

    errors = []

    # Name validation
    if not full_name.strip():
        errors.append("Full name is required.")

    # Date validation: DD/MM/YYYY
    try:
        birth_date = datetime.strptime(dob, "%d/%m/%Y").date()

        if birth_date > date.today():
            errors.append("Date of birth cannot be in the future.")

    except ValueError:
        errors.append("DOB must be a valid date in DD/MM/YYYY format.")

    # Email validation
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(email_pattern, email):
        errors.append("Please enter a valid email address.")

    # Numeric validation
    try:
        if float(glucose) <= 0:
            errors.append("Glucose must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Glucose must be numeric.")

    try:
        if float(haemoglobin) <= 0:
            errors.append("Haemoglobin must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Haemoglobin must be numeric.")

    try:
        if float(cholesterol) <= 0:
            errors.append("Cholesterol must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Cholesterol must be numeric.")

    return errors
