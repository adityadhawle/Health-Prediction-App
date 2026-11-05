from ai_service import generate_health_remarks

try:
    remarks = generate_health_remarks(
        glucose=100,
        haemoglobin=14.5,
        cholesterol=190
    )

    print("\nAI API RESPONSE:\n")
    print(remarks)

except Exception as e:
    print("API Error:", e)