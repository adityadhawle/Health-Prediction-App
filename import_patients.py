import pandas as pd
from validation import validate_patient
from database import add_patient, get_all_patients
from ai_service import generate_health_remarks


def import_patients(file):

    df = pd.read_csv(file)

    required_columns = [
        "full_name", "dob", "email",
        "glucose", "haemoglobin", "cholesterol"
    ]

    if not all(col in df.columns for col in required_columns):
        raise ValueError("CSV file is missing required columns.")

    success_count = 0
    error_count = 0
    duplicate_count = 0
    errors = []

    # Existing database records
    seen = set()

    for patient in get_all_patients():
        p = dict(patient)

        seen.add((
            p["full_name"].strip().lower(),
            p["dob"].strip(),
            p["email"].strip().lower(),
            float(p["glucose"]),
            float(p["haemoglobin"]),
            float(p["cholesterol"])
        ))

    for index, row in df.iterrows():

        try:
            full_name = str(row["full_name"]).strip()
            dob = str(row["dob"]).strip()
            email = str(row["email"]).strip()

            glucose = float(row["glucose"])
            haemoglobin = float(row["haemoglobin"])
            cholesterol = float(row["cholesterol"])

            record = (
                full_name.lower(),
                dob,
                email.lower(),
                glucose,
                haemoglobin,
                cholesterol
            )

            if record in seen:
                duplicate_count += 1
                errors.append({
                    "Row": index + 2,
                    "Patient": full_name,
                    "Errors": "Duplicate record."
                })
                continue

            validation_errors = validate_patient(
                full_name, dob, email,
                glucose, haemoglobin, cholesterol
            )

            if validation_errors:
                error_count += 1
                errors.append({
                    "Row": index + 2,
                    "Patient": full_name,
                    "Errors": "; ".join(validation_errors)
                })
                continue

            try:
                remarks = generate_health_remarks(
                    glucose, haemoglobin, cholesterol
                )
            except Exception:
                remarks = "AI remarks unavailable. Please retry later."

            add_patient(
                full_name, dob, email,
                glucose, haemoglobin, cholesterol,
                remarks
            )

            seen.add(record)
            success_count += 1

        except Exception as error:
            error_count += 1
            errors.append({
                "Row": index + 2,
                "Patient": str(row.get("full_name", "Unknown")),
                "Errors": str(error)
            })

    return success_count, error_count, duplicate_count, errors