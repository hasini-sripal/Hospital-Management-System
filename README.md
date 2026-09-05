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

### Unit Testing
- 27 unit tests covering positive and negative tests

---

## Requirements

- Python 3.x
- openpyxl (for Excel reports)

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

├── main.py                # Main entry point & menu system

├── models.py              # Patient & Doctor business logic

├── HospitalDatabase.py    # Database operations

├── utility.py             # Helper functions & decorators

├── CustomExceptions.py    # Custom exception classes

├── config_loader.py       # Configuration loader

├── logger.py              # Logging setup

├── reports.py             # Excel report generation

├── migration.py           # CSV import script

├── test_hospital.py       # Unit tests

├── config.json            # Configuration file

├── hospital_database.db   # SQLite database (auto-created)

├── hospital.log           # Application log file (auto-created)

├── patient_report.xlsx    # Generated report

├── doctor_report.xlsx     # Generated report

└── summary_workbook.xlsx  # Generated report

---

## Setup

1. Clone or download the project files

2. Install dependencies(for Excel reports):
   ```bash
   pip install openpyxl

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

4. Run the program:
   ```bash
   python main.py

---

## Testing

1. Run all the tests:
   ```bash
   python -m unittest test_hospital.py -v
