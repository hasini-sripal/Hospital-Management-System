from fastapi import FastAPI, HTTPException
from HospitalDatabase import PatientTable, DoctorTable
from Patient import Patient
from Doctor import Doctor
import CustomExceptions
from schemas import (
    PatientCreate, PatientUpdate, AssignDoctor,
    DoctorCreate, DoctorUpdate
)
from datetime import datetime

app = FastAPI(title="Hospital Management System API")

# Initialize Database Tables
patient_db = PatientTable()
doctor_db = DoctorTable()

# Initialize Validators 
patient_validator = Patient()
doctor_validator = Doctor()


# ==========================================
# PATIENT ENDPOINTS
# ==========================================

# 1. GET all patients
@app.get("/patients")
def get_all_patients():
    try:
        return patient_db.view_patient_details()
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="No patients found")

# 2. GET search patients
@app.get("/patients/search")
def search_patients(
    disease: str = None, 
    min_age: int = None, 
    max_age: int = None, 
    doctor_id: int = None
):
    # Edge case: No filters provided
    if not any([disease, min_age is not None, max_age is not None, doctor_id is not None]):
        raise HTTPException(status_code=400, detail="Provide at least one search parameter")
    
    # Edge case: Invalid age range
    if min_age is not None and max_age is not None and min_age > max_age:
        raise HTTPException(status_code=400, detail="min_age cannot be greater than max_age")

    try:
        if disease:
            return patient_db.get_patient_data_by_disease(disease)
        elif min_age is not None and max_age is not None:
            return patient_db.get_patient_data_by_age_range(min_age, max_age)
        elif doctor_id is not None:
            return patient_db.get_patient_data_by_doctor(doctor_id)
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="No matching patients found")
    
# 3. GET patient by ID
@app.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: int):
    try:
        return patient_db.get_patient_data_by_patientid(patient_id)
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Patient not found")


# 4. PUT update patient
@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientUpdate):
    # Check if patient exists
    try:
        patient_db.get_patient_data_by_patientid(patient_id)
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Patient not found")

    try:
        if patient.patient_name is not None:
            patient_validator.check_patient_name_or_disease(patient.patient_name)
            patient_db.update_patient_details(patient_id, patient.patient_name, 'name')
            
        if patient.patient_age is not None:
            patient_validator.check_patient_age(str(patient.patient_age))
            patient_db.update_patient_details(patient_id, patient.patient_age, 'age')
            
        if patient.patient_disease is not None:
            patient_validator.check_patient_name_or_disease(patient.patient_disease)
            patient_db.update_patient_details(patient_id, patient.patient_disease, 'disease')

        return {"message": "Patient updated successfully"}

    except (CustomExceptions.InvalidInputDataError, 
            CustomExceptions.InvalidAgeError) as e:
        raise HTTPException(status_code=422, detail=str(e))



# 5. POST add patient
@app.post("/patients", status_code=201)
def add_patient(patient: PatientCreate):
    try:
        # Validate using existing logic
        patient_validator.check_patient_name_or_disease(patient.patient_name)
        patient_validator.check_patient_age(str(patient.patient_age))
        patient_validator.check_patient_name_or_disease(patient.patient_disease)
        
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        patient_db.insert_patient(
            patient.patient_name,
            patient.patient_age,
            patient.patient_disease,
            created_at
        )
        patient_id = patient_db.get_last_inserted_patient_id()
        return {"message": "Patient added successfully", "patient_id": patient_id}

    except (CustomExceptions.InvalidInputDataError, 
            CustomExceptions.InvalidAgeError, 
            CustomExceptions.InputNotFoundError) as e:
        raise HTTPException(status_code=422, detail=str(e))


# . DELETE patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    try:
        patient_db.get_patient_data_by_patientid(patient_id)
        patient_db.delete_patient_data(patient_id)
        return {"message": "Patient deleted successfully"}
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Patient not found")


# 7. PUT assign doctor
@app.put("/patients/{patient_id}/assign-doctor")
def assign_doctor(patient_id: int, data: AssignDoctor):
    try:
        patient_db.get_patient_data_by_patientid(patient_id)
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    try:
        doctor_db.get_doctor_data_by_doctorid(data.doctor_id)
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patient_db.assign_doctor(patient_id, data.doctor_id)
    return {"message": "Doctor assigned successfully"}


# ==========================================
# DOCTOR ENDPOINTS
# ==========================================

# 8. GET all doctors
@app.get("/doctors")
def get_all_doctors():
    try:
        return doctor_db.view_doctor_details()
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="No doctors found")

# 9. GET search doctors
@app.get("/doctors/search")
def search_doctors(
    name: str = None,
    specialization: str = None
):
    if not any([name, specialization]):
        raise HTTPException(status_code=400, detail="Provide at least one search parameter")

    try:
        if name:
            doctor_validator.check_if_doctor_name_exists(name)
            return doctor_db.get_doctor_data_by_name(name)

        elif specialization:
            doctor_validator.check_if_doctor_specialization_exists(specialization)
            return doctor_db.get_doctor_data_by_specialization(specialization)
            
        elif doctor_id is not None:
            patient_validator.check_if_assigned_doctor_id_exists(doctor_id)
            return patient_db.get_patient_data_by_doctor(doctor_id)

    except CustomExceptions.PatientDiseaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CustomExceptions.PatientAgeRangeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CustomExceptions.DoctorIDNotFoundInPatientDatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 10. GET doctor by ID
@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    try:
        doctor = doctor_db.get_doctor_data_by_doctorid(doctor_id)
        return doctor
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail=f"Doctor with ID {doctor_id} not found")
    except Exception as e:
        # Edge case: Any other unexpected error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# 11. POST add doctor
@app.post("/doctors", status_code=201)
def add_doctor(doctor: DoctorCreate):
    try:
        # Validate using existing logic
        doctor_validator.check_doctor_name_or_specialization(doctor.doctor_name)
        doctor_validator.check_doctor_name_or_specialization(doctor.doctor_specialisation)
        
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doctor_db.insert_doctor(
            doctor.doctor_name,
            doctor.doctor_specialisation,
            created_at
        )
        doctor_id = doctor_db.get_last_inserted_doctor_id()
        return {"message": "Doctor added successfully", "doctor_id": doctor_id}

    except (CustomExceptions.InvalidInputDataError, 
            CustomExceptions.InputNotFoundError) as e:
        raise HTTPException(status_code=422, detail=str(e))


# 12. PUT update doctor
@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor: DoctorUpdate):
    try:
        doctor_db.get_doctor_data_by_doctorid(doctor_id)
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if doctor.doctor_name is None and doctor.doctor_specialisation is None:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    try:
        if doctor.doctor_name is not None:
            doctor_validator.check_doctor_name_or_specialization(doctor.doctor_name)
            doctor_db.update_doctor_data(doctor_id, doctor.doctor_name, 'name')
            
        if doctor.doctor_specialisation is not None:
            doctor_validator.check_doctor_name_or_specialization(doctor.doctor_specialisation)
            doctor_db.update_doctor_data(doctor_id, doctor.doctor_specialisation, 'specialisation')

        return {"message": "Doctor updated successfully"}

    except (CustomExceptions.InvalidInputDataError, 
            CustomExceptions.InputNotFoundError) as e:
        raise HTTPException(status_code=422, detail=str(e))


# 13. DELETE doctor
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    try:
        doctor_db.get_doctor_data_by_doctorid(doctor_id)
        doctor_db.delete_doctor_data(doctor_id)
        return {"message": "Doctor deleted successfully"}
    except CustomExceptions.RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Doctor not found")