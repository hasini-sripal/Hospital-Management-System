# Hospital Management System

A Python-based Hospital Management System built with OOP and SQLite.

---

## Features

### Patient Management
- Add new patients
- View all patients
- Search patients (ID, Name, Disease, Doctor)
- Update patient details (Name, Age, Disease, Doctor)
- Delete patients
- Assign Doctor

### Doctor Management
- Add new doctors
- View all doctors
- Search doctors by ID or Name
- Update doctor details (Name, Specialisation)
- Delete doctors

### Simple Report
- Patient per Doctor Count
- Most common disease
- Most common age

### Logging
- All add, update, and delete actions are logged to `hospital.log` with timestamps
- Performance management with @timer decorator

### Excel Reports
- The system generates professional Excel reports with auto-sized columns, bold headers, and center-aligned formatting.
- Reports generated: patient_report.xlsx, doctor_report.xlsx, summary_workbook.xlsx


### REST API (Task 4)
- FastAPI Framework: Full CRUD REST API for both Patients and Doctors.

- Pydantic Validation: Strict request body validation (returns 422 Unprocessable Entity for invalid data).

- Advanced Error Handling: Returns 404 Not Found for missing IDs, 400 Bad Request for invalid search ranges, and reuses existing business logic for age/name validation.

- Swagger UI: Interactive auto-generated API documentation available at /docs.
---

## Requirements

- Python 3.x
- openpyxl (for Excel reports)
- fastapi 

---
## Configuration
Create a config.json file:
{
    "database": "hospital_database.db",
    "log_file": "hospital.log",
    "max_input_tries": 5,
    "hospital_name": "City Hospital"
}

---

## Project Structure

├── main.py                # Terminal UI entry point (CLI)

├── main_api.py            # FastAPI application (REST API)

├── schemas.py             # Pydantic models for API validation

├── models.py              # Patient & Doctor logic

├── HospitalDatabase.py    # SQLite database operations

├── utility.py             # Helper functions & decorators

├── CustomExceptions.py    # Custom exception classes

├── config_loader.py       # Configuration loader

├── logger.py              # Logging setup

├── reports.py             # Excel report generation

├── test_hospital.py       # Unit tests (27 tests)

├── migration.py           # CSV import script

├── config.json            # Configuration file

├── hospital_database.db   # SQLite database (auto-created)

└── hospital.log           # Application log file (auto-created)

---

## Setup

1. Clone or download the project files

2. Install dependencies(for Excel reports):
   ```bash
   pip install fastapi uvicorn openpyxl

3. Ensure all files are in the same folder:
   - `models.py`
   - `HospitalDatabase.py`
   - `utility.py`
   - `CustomExceptions.py`
   - `main.py`
   - `hospital_database.db`
   - `migrationscript.py`
   - `logger.py`
   - `Patient.py`
   - `Doctor.py`
   - `hospital.log`
   - `reports.py`
   - `config_loader.py`
   - `main_api.py`
   - `schema.py`

4. Run the program:
   ```bash
   python main.py

---

## Testing

1. Run all the tests:
   ```bash
   python -m unittest test_hospital.py -v

## REST API
1. To start the API server
   ```bash
   python -m uvicorn main_api:app --reload
   
- Once running, open your browser and go to:
- http://127.0.0.1:8000/docs to access the Swagger UI where you can test all endpoints.

## Postman Testing

### To test the API manually:

- Import the Hospital Management System API.postman_collection.json file into Postman.
- Ensure the FastAPI server is running.
- Execute the 13 pre-configured requests to verify all status codes and responses.

