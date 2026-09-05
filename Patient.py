"""
Module that handles Patient Management System
"""

import config_loader, logger, utility, CustomExceptions, HospitalDatabase
from datetime import datetime

class Patient:
    """
    Class that represents a patient in the Hospital Management System
    """
    def __init__(self) -> None:
        """
        Constructor for the Patient class. Initializes the patient name, age, and disease.
        """
        self.patient_database = HospitalDatabase.PatientTable()
        config = config_loader.load_config('config.json')
        self.MAX_TRIES = config.get("max_input_tries", 5)
        self.hospital_logger = logger.get_logger()
        self.patient_name = None
        self.patient_age = None
        self.patient_disease = None
        self.assigned_doctor_id = None
        self.patient_id = None
        self.created_at = None

    def __str__(self) -> str:
        """
        String representation of the Patient class. Returns the patient name, age, and disease.
        """
        return (f"Patient [{self.patient_id}: {self.patient_name}], "
                f"Patient Age: {self.patient_age}, "
                f"Patient Disease: {self.patient_disease}, "
                f"Assigned Doctor ID: {self.assigned_doctor_id}")

    def __repr__(self) -> str:
        """
        Representation of the Patient class. Returns the patient name, age, and disease.
        """
        return (f"Patient(id={self.patient_id}, name={self.patient_name!r}, "
            f"age={self.patient_age}, disease={self.patient_disease!r}, "
            f"assigned_doctor_id={self.assigned_doctor_id!r})")

    def check_patient_name_or_disease(self, patient_data:str) -> None:
        """
        Checks if the patient name or disease:
        1. is entered by the user
        2. contains only alphabets and spaces
        """        
        patient_data = patient_data.strip()
        if not patient_data:
            raise CustomExceptions.InputNotFoundError()
        if not all(c.isalpha() or c.isspace() or c in "'-" for c in patient_data):
            raise CustomExceptions.InvalidInputDataError(patient_data)
    
    def check_patient_age(self, patient_age:str) -> None:
        """
        Checks that the patient age:
        1. Is entered by the user
        2. Contains only integer
        3. Does not exceed 130 years
        """
        if not patient_age.strip():
            raise CustomExceptions.InputNotFoundError() 
        elif not patient_age.isdigit():
            raise CustomExceptions.InvalidAgeError(patient_age)
        elif not int(patient_age) <= 130:
            raise CustomExceptions.AgeExceedsLimitError(patient_age)
    
    def check_if_patient_name_exists(self, patient_name:str) -> None:
        """
        Checks if the patient's name exists in the database
        """
        patient_data = self.patient_database.view_patient_details()
        if any(data[2] == patient_name for data in patient_data):
            return
        raise CustomExceptions.PatientNameNotFoundError(patient_name)
        
    def check_if_patient_disease_exists(self, patient_disease:str) -> None:
        """
        Checks if the patient's name exists in the database
        """
        patient_data = self.patient_database.view_patient_details()
        if any(data[4] == patient_disease for data in patient_data):
            return
        raise CustomExceptions.PatientDiseaseNotFoundError(patient_disease)
        
    def check_if_assigned_doctor_id_exists(self, doctor_id:str) -> None:
        """
        Checks if the assigned doctor id exists in the database
        """
        patient_data = self.patient_database.view_patient_details()
        if any(data[1] == int(doctor_id) for data in patient_data):
            return
        raise CustomExceptions.DoctorIDNotFoundInPatientDatabaseError(doctor_id)
    
    def check_if_patient_agerange_exists(self, min_age:int, max_age:int) -> None:
        """
        Checks if the assigned doctor id exists in the database
        """
        if min_age >= max_age:
            raise CustomExceptions.InvalidMinAgeError(min_age, max_age)
        
        patient_data = self.patient_database.view_patient_details()
        if any(min_age <= data[3] <= max_age for data in patient_data):
            return
        raise CustomExceptions.PatientAgeRangeNotFound(min_age,max_age)
        
    def check_patient_id(self,patient_id:str) -> None:
        """
        Checks if the patient id:
        1. Exists in the database
        2. Is entered by the user
        3. Contains only integers
        """
        if not patient_id.strip():
            raise CustomExceptions.InputNotFoundError()
        if not patient_id.isdigit():
            raise CustomExceptions.InvalidPatientIDError(patient_id)
    
        consolidated_patient_ids = self.patient_database.view_patient_details()
        if any(patient_data[0] == int(patient_id) for patient_data in consolidated_patient_ids):
            return
        raise CustomExceptions.PatientIDNotFoundError(patient_id)

    def check_doctor_id(self,doctor_id:str) -> None:
        """
        Checks if the doctor id:
        1. Exists in the database
        2. Is entered by the user
        3. Contains only integers
        """
        if not doctor_id.strip():
            raise CustomExceptions.InputNotFoundError()
    
        if not doctor_id.isdigit():
            raise CustomExceptions.InvalidDoctorIDError(doctor_id)
            
        consolidated_doctor_ids = HospitalDatabase.DoctorTable().view_doctor_details()
        if any(doctor_data[0] == int(doctor_id) for doctor_data in consolidated_doctor_ids):
            return
        raise CustomExceptions.DoctorIDNotFoundError(doctor_id)

    def check_doctor_name(self,doctor_name:str) -> None:
        """
        Checks if the doctor name:
        1. Exists in the database
        2. Is entered by the user
        3. Contains only alphabets
        """
        doctor_name = doctor_name.strip()
        if not doctor_name:
            raise CustomExceptions.InputNotFoundError()
        if not all(c.isalpha() or c.isspace() or c in "'-" for c in doctor_name):
            raise CustomExceptions.InvalidInputDataError(doctor_name)
        
        doctor_data = HospitalDatabase.DoctorTable().view_doctor_details()
        if any(name[1] == doctor_name for name in doctor_data):
            return
        raise CustomExceptions.DoctorNameNotFoundError(doctor_name)
    
    @utility.log_action 
    def add_patient(self, patient_name:str, patient_age:int, patient_disease:str) -> None:
        """
        Add a new patient to the database. This function will create a new patient ID and insert the patient data into the database.
        Getting the patient's name by checking if the input is valid. 
        If the input is invalid even after 5 tries, the input is completely discarded
        """
        self.patient_name = patient_name.strip()
        self.patient_age = patient_age
        self.patient_disease = patient_disease.strip()
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.patient_database.insert_patient(self.patient_name, self.patient_age, self.patient_disease, self.created_at)

        self.patient_id = self.patient_database.get_last_inserted_patient_id()
        print("Patient Added Successfully!")
        self.hospital_logger.info(f"Patient Name:{patient_name}, Patient Age:{patient_age}, Disease: {patient_disease} added into Patient Table")
        
    @utility.log_action 
    @utility.timer
    def view_patient_details(self) -> None:
        """
        Function to view all the patient details from the database.
        """
        try:
            patient_details = self.patient_database.view_patient_details()
            for patient_data in patient_details:
               self._display_patient(patient_data)
            
        
        except CustomExceptions.RecordNotFoundError as e:
            print (f"Error: {e}")
        except Exception as e:
            print (f"Error: {e}")

    @utility.log_action 
    def delete_patient_details(self,patient_id:int) -> None:
        """
        Delete a patient's details from the database based on the patient ID. 
        This function will prompt the user to enter a patient ID and delete the corresponding patient data from the database.
        """
        try:
            self.patient_database.delete_patient_data(patient_id)
            print("Patient Deleted Successfully!")
            self.hospital_logger.info(f"Patient ID:{patient_id} is deleted")
        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def search_for_patient_by_id(self,patient_id:int) -> None:
        """
        Searches patient data by the ID entered
        If the ID is not found, an error message is displayed.
        """
        try:
            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            self._display_patient(patient_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action     
    def search_for_patient_by_name(self, patient_name:str) -> None:
        """
        Searches patient data by the name entered. If many matching data are found, all of them are displayed
        If the name is not found, an error message is displayed.
        """
        try:
            patient_details = self.patient_database.get_patient_data_by_name(patient_name)
            for patient_data in patient_details:
                self._display_patient(patient_data)

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def search_for_patient_by_disease(self,patient_disease:str) -> None:
        """
        Searches patient data by the disease entered. If many matching data are found, all of them are displayed
        If the disease is not found, an error message is displayed.
        """
        try:
            patient_details = self.patient_database.get_patient_data_by_disease(patient_disease)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)
        
        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action    
    def search_for_patient_by_agerange(self, min_age:int, max_age:int) -> None:
        """
        Searches patient data by the age range entered. If many matching data are found, all of them are displayed
        If the age range is not found, an error message is displayed.
        """
        try:
            patient_details = self.patient_database.get_patient_data_by_age_range(min_age, max_age)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)
        except Exception as e:
            print(f"Error: {e}")        

    @utility.log_action 
    def search_for_patient_by_doctor(self, doctor_id:int) -> None:
        """
        Searches patient data by the doctor_id entered. If many matching data are found, all of them are displayed
        If the doctor id is not found, an error message is displayed.
        """
        try:
            self.check_if_assigned_doctor_id_exists(int(doctor_id))
            patient_details = self.patient_database.get_patient_data_by_doctor(doctor_id)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def update_patient_name(self,patient_id:int,patient_name:str) -> None:
        """
        Updates the patient name by the patient id entered
        """
        try:
            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            if patient_data[2] == patient_name.strip():
                print("Patient name matches. No changes made.")
                return
            
            self.patient_database.update_patient_details(patient_id, patient_name.strip(), 'name')
            print("Patient name updated successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id}'s name changed to {patient_name}")

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action  
    def update_patient_age(self, patient_id:int, patient_age:int) -> None:
        """
        Updates the patient details by the patient id entered
        """
        try:
            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            if patient_data[3] == int(patient_age):
                print("Patient age matches. No changes made.")
                return

            self.patient_database.update_patient_details(int(patient_id), int(patient_age), 'age')
            print("Patient age updated successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id}'s age changed to {patient_age}")

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action
    def update_patient_disease(self,patient_id:int, patient_disease:str) -> None:
        """
        Updates the patient disease by the patient id entered
        """
        try:
            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            if patient_data[4] == patient_disease.strip():
                print("Patient disease matches. No changes made.")
                return

            self.patient_database.update_patient_details(int(patient_id), patient_disease.strip(), 'disease')
            print("Patient disease updated successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id}'s disease changed to {patient_disease}")

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action
    def patient_count_per_doctor(self, doctor_id:int) -> None:
        """
        Displays the patient count of a doctor by doctor id
        """
        try:
            patient_count = self.patient_database.patient_per_doctor_count(doctor_id)
            print(f"Number of patients: {patient_count[0]}")

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action
    def most_common_disease(self) -> None:
        """
        Displays the most common disease along with the number of patients affected by it
        If there are disease with the same count, all of them are displayed
        """
        try:
            most_disease = self.patient_database.most_common_disease()
            NO_OF_MOST_COMMON_DISEASE = len(most_disease)

            for i in range(1,NO_OF_MOST_COMMON_DISEASE+1):
                print(f"S.No: {i}")
                disease = most_disease[i-1]
                print(f"Disease: {disease[0]}, Number of patients: {disease[1]}")

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def most_common_age(self) -> None:
        """
        Displays the most common age along with the number of patients of that age
        If there are age(s) with the same count, all of them are displayed
        """
        try:
            most_age = self.patient_database.most_common_age()
            NO_OF_MOST_COMMON_AGE = len(most_age)

            for i in range(1, NO_OF_MOST_COMMON_AGE+1):
                print(f"S.No: {i}")
                age = most_age[i-1]
                print(f"Age: {age[0]}, Number of patients: {age[1]}")

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def assign_doctor(self,patient_id:int, doctor_name) -> None:
        """
        Assign a doctor to a patient.

        *args:
            patient_id: ID of the patient
            doctor_name: Name of the doctor to assign

        If multiple doctors share the same name, all are displayed with their details.
        User selects the correct doctor by ID.
        """    
        try:            
            doctor_data = HospitalDatabase.DoctorTable().get_doctor_data_by_name(doctor_name)
            for data in doctor_data:
                print(f"Doctor ID:{data[0]}, Specialisation:{data[2]}")
            
            doctor_id = utility.get_input_with_retry(
                "Doctor ID: ",
                self.check_doctor_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidDoctorIDError,
                 CustomExceptions.DoctorIDNotFoundError)
            )
            if doctor_id is None:
                return

            self.patient_database.update_patient_details(int(patient_id), int(doctor_id), 'doctor' )
            print("Doctor Assigned Successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id} is assigned to Doctor ID:{doctor_id}")

        except Exception as e:
            print(f"Error: {e}")   

    def _display_patient(self, patient_data:tuple) -> None:
        """Helper to display patient details"""
        print(f"Patient ID: {patient_data[0]}, "
              f"Patient Name: {patient_data[2]}, "
              f"Patient Age: {patient_data[3]}, "
              f"Patient Disease: {patient_data[4]}, "
              f"Assigned Doctor ID: {patient_data[1]},"
              f"Time of Admission: {patient_data[5]}")
