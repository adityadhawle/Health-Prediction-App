
import sqlite3

DB_NAME = "health_prediction.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            ai_remarks TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def add_patient(full_name, dob, email, glucose,
                haemoglobin, cholesterol, ai_remarks=""):

    conn = get_connection()

    conn.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose, haemoglobin,
         cholesterol, ai_remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        full_name, dob, email, glucose,
        haemoglobin, cholesterol, ai_remarks
    ))

    conn.commit()
    conn.close()


def get_all_patients():
    conn = get_connection()
    patients = conn.execute(
        "SELECT * FROM patients ORDER BY id"
    ).fetchall()
    conn.close()

    return patients


def update_patient(patient_id, full_name, dob, email,
                   glucose, haemoglobin, cholesterol,
                   ai_remarks=""):

    conn = get_connection()

    conn.execute("""
        UPDATE patients
        SET full_name=?, dob=?, email=?, glucose=?,
            haemoglobin=?, cholesterol=?, ai_remarks=?
        WHERE id=?
    """, (
        full_name, dob, email, glucose,
        haemoglobin, cholesterol, ai_remarks, patient_id
    ))

    conn.commit()
    conn.close()


def delete_patient(patient_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )

    conn.commit()
    conn.close()
