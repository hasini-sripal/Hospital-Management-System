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

---

## Requirements

- Python 3.x
- No external libraries needed (uses built-in sqlite3)

---
## Project Structure

├── main.py # Entry point
├── Patient.py # Patient class
├── Doctor.py # Doctor class
├── hospital.py # Hospital class (main controller)
├── HosptalDatabase.py # SQLite database operations
├── utility.py # Helper functions
├── CustomExceptions.py # Custom exceptions
├── logger.py # Logging setup
├── migrationscript.py # One-time migration script
├── hospital.log # Log file (created automatically)
└── hospital_database.db # SQLite database (created automatically)

---

## Setup

1. Clone or download the project files

2. Ensure all files are in the same folder:
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

3. Run the program:
   ```bash
   python main.py