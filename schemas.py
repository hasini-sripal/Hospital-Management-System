from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    patient_name: str
    patient_age: int
    patient_disease: str

class PatientUpdate(BaseModel):
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_disease: Optional[str] = None

class DoctorCreate(BaseModel):
    doctor_name: str
    doctor_specialisation: str

class DoctorUpdate(BaseModel):
    doctor_name: Optional[str] = None
    doctor_specialisation: Optional[str] = None

class AssignDoctor(BaseModel):
    doctor_id: int




    
