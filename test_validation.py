
from validation import validate_patient

# Valid patient
errors = validate_patient(
    "John Smith",
    "15/08/1995",
    "john@gmail.com",
    100,
    14.5,
    190
)

print("Valid patient errors:", errors)

# Invalid patient
errors = validate_patient(
    "Test Patient",
    "19/10/2030",
    "hunter@gmail",
    100,
    14.5,
    190
)

print("Invalid patient errors:", errors)
