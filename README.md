# 🏥 Health Prediction Application

A Python-based Health Prediction Application that manages patient records, validates blood test information, and generates AI-assisted health observations using the Groq API.

## 📌 Project Overview

The application allows users to manage patient information and blood test results through an interactive Streamlit interface.

It uses SQLite for persistent data storage and integrates an external AI API to generate informational remarks based on blood test values.

**Important:** AI-generated remarks are for informational purposes only and are not medical diagnoses.

## ✨ Features

- **Patient Management (CRUD)**
  - Add new patient records
  - View patient records
  - Update existing patient details
  - Delete patient records

- **AI Health Remarks**
  - Integration with Groq API
  - AI-generated observations based on blood test values
  - Remarks stored with patient records

- **Input Validation**
  - Full name validation
  - Email format validation
  - Date of birth validation
  - Future date prevention
  - Numeric blood test value validation

- **CSV Import**
  - Upload patient records through CSV files
  - Preview uploaded data
  - Validate imported records
  - Detect duplicate records
  - Generate AI remarks for valid records
  - Display import error reports

- **Database**
  - SQLite database
  - Persistent patient record storage

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Web application interface |
| SQLite | Database |
| Pandas | CSV processing and data handling |
| Groq API | AI-generated health observations |
| Requests | API communication |
| Python-dotenv | Environment variable management |

## 📂 Project Structure

```text
Health-Prediction-App/
│
├── app.py
├── database.py
├── validation.py
├── ai_service.py
├── import_patients.py
│
├── test_validation.py
├── test_ai.py
├── check_models.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

The SQLite database file is generated automatically when the application runs.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/adityadhawle/Health-Prediction-App.git
cd Health-Prediction-App
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get an API key from the Groq developer platform:

https://console.groq.com/

**Security:** Never upload your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧪 Testing

Run the validation tests:

```bash
python test_validation.py
```

Test the AI API integration:

```bash
python test_ai.py
```

Check Python syntax:

```bash
python -m py_compile app.py database.py validation.py ai_service.py import_patients.py
```

## 📊 Patient Data Fields

The application manages the following information:

| Field | Description |
|---|---|
| Full Name | Patient's full name |
| DOB | Date of birth |
| Email | Patient email address |
| Glucose | Blood glucose (mg/dL) |
| Haemoglobin | Haemoglobin (g/dL) |
| Cholesterol | Cholesterol (mg/dL) |
| AI Remarks | AI-generated informational observations |

The displayed units are assumptions used by the application. Actual interpretation depends on laboratory reference ranges and clinical context.

## 🤖 AI Integration

The application integrates the Groq API to generate observations from:

- Glucose
- Haemoglobin
- Cholesterol

The AI response provides cautious informational observations and recommends consulting a qualified healthcare professional.

It is not a clinically validated diagnostic system.

## 🔐 Data Security

- API credentials are stored in environment variables.
- `.env` is excluded from Git using `.gitignore`.
- The SQLite database is excluded from Git.
- Virtual environment files are excluded from Git.

## 👨‍💻 Author

**Aditya Dhawle**

B.Tech – Electronics and Telecommunication Engineering

## 📄 License

This project was developed as part of a technical assessment.
