
import streamlit as st
import pandas as pd
import database
from validation import validate_patient
from ai_service import generate_health_remarks
from datetime import date, datetime
from import_patients import import_patients

# Page configuration
st.set_page_config(
    page_title="Health Prediction App",
    page_icon="🏥",
    layout="wide"
)

# Initialize database
database.create_table()

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #17365D;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏥 Health Prediction")
st.sidebar.caption("Patient Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Patient",
        "Patient Records",
        "Update Patient",
        "Delete Patient",
        "Import Patients"
    ]
)

# Fetch patients
patients = [dict(p) for p in database.get_all_patients()]


def generate_remarks(glucose, haemoglobin, cholesterol):
    try:
        with st.spinner("AI is analysing the blood test values..."):
            return generate_health_remarks(
                glucose, haemoglobin, cholesterol
            )
    except Exception as error:
        st.error(f"AI remarks could not be generated: {error}")
        return "AI remarks unavailable. Please retry later."


def show_errors(errors):
    for error in errors:
        st.error(error)


# DASHBOARD
if page == "Dashboard":

    st.title("🏥 Health Prediction Dashboard")
    st.write("Patient health records and AI-generated observations.")

    total = len(patients)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", total)
    col2.metric(
        "Average Glucose",
        f"{sum(p['glucose'] for p in patients) / total:.1f}"
        if total else "N/A"
    )
    
    page = st.sidebar.radio
    col3.metric(
        "Average Cholesterol",
        f"{sum(p['cholesterol'] for p in patients) / total:.1f}"
        if total else "N/A"
    )

    st.subheader("Recent Patient Records")

    if patients:
        df = pd.DataFrame(patients)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No patient records available yet.")


# ADD PATIENT
elif page == "Add Patient":

    st.title("➕ Add New Patient")
    st.write("Enter patient details and blood test results.")

    with st.form("add_patient_form"):

        full_name = st.text_input("Full Name")

        dob = st.date_input(
            "Date of Birth",
            value=date(1995, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )

        email = st.text_input("Email Address")

        col1, col2, col3 = st.columns(3)

        glucose = col1.number_input(
            "Glucose (mg/dL)", min_value=0.0, value=100.0
        )

        haemoglobin = col2.number_input(
            "Haemoglobin (g/dL)", min_value=0.0, value=14.0
        )

        cholesterol = col3.number_input(
            "Cholesterol (mg/dL)", min_value=0.0, value=190.0
        )

        submitted = st.form_submit_button(
            "Save Patient & Generate AI Remarks",
            use_container_width=True
        )

    if submitted:

        dob_string = dob.strftime("%d/%m/%Y")

        errors = validate_patient(
            full_name, dob_string, email,
            glucose, haemoglobin, cholesterol
        )

        if errors:
            show_errors(errors)

        else:
            remarks = generate_remarks(
                glucose, haemoglobin, cholesterol
            )

            database.add_patient(
                full_name.strip(),
                dob_string,
                email.strip(),
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )

            st.success("Patient record saved successfully!")
            st.info("AI remarks have been saved with the patient record.")
            st.rerun()


# VIEW PATIENTS
elif page == "Patient Records":

    st.title("📋 Patient Records")

    if patients:
        df = pd.DataFrame(patients)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("View AI Health Remarks")

        patient_ids = [p["id"] for p in patients]

        selected_id = st.selectbox(
            "Select Patient ID",
            patient_ids
        )

        selected = next(
            p for p in patients if p["id"] == selected_id
        )

        st.write(f"**Patient:** {selected['full_name']}")
        st.write(selected["ai_remarks"] or "No AI remarks available.")

    else:
        st.info("No patient records found.")


# UPDATE PATIENT
elif page == "Update Patient":

    st.title("✏️ Update Patient Details")

    if patients:

        patient_map = {p["id"]: p for p in patients}

        selected_id = st.selectbox(
            "Select Patient",
            list(patient_map.keys()),
            format_func=lambda pid: (
                f"ID {pid} - {patient_map[pid]['full_name']}"
            )
        )

        selected = patient_map[selected_id]

        try:
            current_dob = datetime.strptime(
                selected["dob"], "%d/%m/%Y"
            ).date()
        except ValueError:
            current_dob = date(1995, 1, 1)

        with st.form("update_patient_form"):

            full_name = st.text_input(
                "Full Name", value=selected["full_name"]
            )

            dob = st.date_input(
                "Date of Birth",
                value=min(current_dob, date.today()),
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

            email = st.text_input(
                "Email Address", value=selected["email"]
            )

            col1, col2, col3 = st.columns(3)

            glucose = col1.number_input(
                "Glucose (mg/dL)",
                min_value=0.0,
                value=float(selected["glucose"])
            )

            haemoglobin = col2.number_input(
                "Haemoglobin (g/dL)",
                min_value=0.0,
                value=float(selected["haemoglobin"])
            )

            cholesterol = col3.number_input(
                "Cholesterol (mg/dL)",
                min_value=0.0,
                value=float(selected["cholesterol"])
            )

            update = st.form_submit_button(
                "Update Patient",
                use_container_width=True
            )

        if update:

            dob_string = dob.strftime("%d/%m/%Y")

            errors = validate_patient(
                full_name, dob_string, email,
                glucose, haemoglobin, cholesterol
            )

            if errors:
                show_errors(errors)

            else:
                remarks = generate_remarks(
                    glucose, haemoglobin, cholesterol
                )

                database.update_patient(
                    selected_id,
                    full_name.strip(),
                    dob_string,
                    email.strip(),
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                )

                st.success("Patient updated successfully!")
                st.rerun()

    else:
        st.info("No patients available to update.")


# DELETE PATIENT
elif page == "Delete Patient":

    st.title("🗑️ Delete Patient")

    if patients:

        patient_map = {p["id"]: p for p in patients}

        selected_id = st.selectbox(
            "Select Patient to Delete",
            list(patient_map.keys()),
            format_func=lambda pid: (
                f"ID {pid} - {patient_map[pid]['full_name']}"
            )
        )

        selected = patient_map[selected_id]

        st.warning(
            f"You selected: {selected['full_name']} "
            f"(ID: {selected_id})"
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this patient."
        )

        if st.button(
            "Delete Patient",
            disabled=not confirm
        ):
            database.delete_patient(selected_id)
            st.success("Patient deleted successfully!")
            st.rerun()

    else:
        st.info("No patients available to delete.")

# IMPORT PATIENTS
elif page == "Import Patients":
    st.write("Import Patients section reached")

    st.title("📂 Import Patient Records")

    st.write("Upload the assessment CSV file.")

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.subheader("CSV Preview")

        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        if st.button("Import Patients"):

            uploaded_file.seek(0)

            with st.spinner("Importing patients and generating AI remarks..."):

                success, errors, duplicates, error_details = (
                    import_patients(uploaded_file)
                )

            st.success(f"Successfully imported: {success}")
            st.warning(f"Invalid records: {errors}")
            st.info(f"Duplicate records skipped: {duplicates}")

            if error_details:
                st.subheader("Import Error Report")
                st.dataframe(
                    pd.DataFrame(error_details),
                    use_container_width=True
                )

            

        
