"""
Custom Exceptions for Hospital Management System
"""


class PatientIDNotFoundError(Exception):
    
    def __init__(self, patient_id:str) -> None:
        self.patient_id = patient_id
        self.message = f"Patient ID {self.patient_id} not found"
        super().__init__(self.message)

class InvalidPatientIDError(Exception):
    def __init__(self, patient_id:str) -> None:
        self.patient_id = patient_id
        self.message = f"Invalid Patient ID: {self.patient_id}"
        super().__init__(self.message)

class InvalidInputDataError(Exception):
    def __init__(self, patient_or_doctor_data:str) -> None:
        self.message = f"Input contains special character or number: {patient_or_doctor_data}"
        super().__init__(self.message)

class InvalidAgeError(Exception):
    def __init__(self, age:str) -> None:
        self.age = age
        self.message = f"Input contains special characters or alphabets: {self.age}"
        super().__init__(self.message)

class InputNotFoundError(Exception):
    def __init__(self) -> None:
        self.message = "Input not found. Please provide the required input"
        super().__init__(self.message)

class RecordNotFoundError(Exception):
    def __init__(self) -> None:
        self.message = f"Record does not exist. Check again!"
        super().__init__(self.message)

class InvalidDoctorIDError(Exception):
    def __init__(self, doctor_id:str) -> None:
        self.doctor_id = doctor_id
        self.message = f"Invalid Doctor ID: {self.doctor_id}"
        super().__init__(self.message)

class DoctorIDNotFoundError(Exception):
    def __init__(self, doctor_id:str) -> None:
        self.doctor_id = doctor_id
        self.message = f"Doctor ID {self.doctor_id} not found"
        super().__init__(self.message)

class PatientNameNotFoundError(Exception):
    def __init__(self, patient_name:str) -> None:
        self.patient_name = patient_name
        self.message = f"Patient Name: {self.patient_name} not found"
        super().__init__(self.message)

class DoctorNameNotFoundError(Exception):
    def __init__(self, doctor_name:str) -> None:
        self.doctor_name = doctor_name
        self.message = f"Doctor Name: {self.doctor_name} not found"
        super().__init__(self.message)

class DoctorIDNotFoundInPatientDatabaseError(Exception):
    def __init__(self, doctor_id:str) -> None:
        self.doctor_id = doctor_id
        self.message = f"Doctor ID: {self.doctor_id} not found in Patient Database"
        super().__init__(self.message)

class PatientAgeRangeNotFound(Exception):
    def __init__(self, min_age:str, max_age:str) -> None:
        self.min_age, self.max_age = min_age, max_age
        self.message = f"Age Range: between {self.min_age} and {self.max_age} not found"
        super().__init__(self.message)

class PatientDiseaseNotFoundError(Exception):
    def __init__(self, patient_disease:str) -> None:
        self.patient_disease = patient_disease
        self.message = f"Patient Disease: {self.patient_disease} not found"
        super().__init__(self.message)

class AgeExceedsLimitError(Exception):
    def __init__(self, patient_age:str) -> None:
        self.patient_age = patient_age
        self.message = f"Patient age: {self.patient_age} cannot be more than 130 years"
        super().__init__(self.message)

class InvalidMinAgeError(Exception):
    def __init__(self, min_age:str, max_age:str) -> None:
        self.min_age , self.max_age = min_age, max_age
        self.message = f"Minimum Age: {self.min_age} is greater than or equal to Maximum Age: {self.max_age}"
        super().__init__(self.message)

class InvalidPatientCountError(Exception):
    def __init__(self, no_of_patients:str) -> None:
        self.no_of_patients = no_of_patients
        self.message = f"Invalid Patient Count: {self.no_of_patients}. It should be a positive integer."
        super().__init__(self.message)
