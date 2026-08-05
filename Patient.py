"""
Module that handles Patient Management System
"""

import HospitalDatabase
import CustomExceptions
import utility
import logger

class Patient:
    """
    Class that represents a patient in the Hospital Management System
    """
    def __init__(self):
        """
        Constructor for the Patient class. Initializes the patient name, age, and disease.
        """
        self.patient_database = HospitalDatabase.PatientTable()
        self.MAX_TRIES = 5                             #no. of tries allowed to the user incase the input is invalid
        self.hospital_logger = logger.get_logger()

    def check_patient_name_or_disease(self, patient_data):
        """
        Checks if the patient name or disease:
        1. is entered by the user
        2. contains only alphabets
        """        
        patient_data_without_spaces = ''.join(patient_data.split())          
        if not patient_data_without_spaces.strip():                 
            raise CustomExceptions.InputNotFoundError()
        if not patient_data_without_spaces.isalpha():
            raise CustomExceptions.InvalidInputDataError(patient_data) 
    
    def check_patient_age(self, patient_age):
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
    
    def check_if_patient_name_exists(self, patient_name):
        """
        Checks if the patient's name exists in the database
        """
        patient_data = self.patient_database.view_patient_details()
        for data in patient_data:
            if data[2] == patient_name:
                return
        else:
            raise CustomExceptions.PatientNameNotFoundError(patient_name)
        
    def check_if_patient_disease_exists(self, patient_disease):
        """
        Checks if the patient's name exists in the database
        """
        patient_data = self.patient_database.view_patient_details()
        for data in patient_data:
            if data[4] == patient_disease:
                return
        else:
            raise CustomExceptions.PatientDiseaseNotFoundError(patient_disease)
        
    def check_if_assigned_doctor_id_exists(self, doctor_id):
        """
        Checks if the assigned doctor id exists in the database
        """
        patient_data = self.patient_database.view_patient_details()
        for data in patient_data:
            if data[1] == doctor_id:
                return
        else:
            raise CustomExceptions.DoctorIDNotFoundInPatientDatabaseError(doctor_id)
    
    def check_if_patient_agerange_exists(self, min_age, max_age):
        """
        Checks if the assigned doctor id exists in the database
        """
        if min_age >= max_age:
            raise CustomExceptions.InvalidMinAgeError(min_age, max_age)
            return
        
        patient_data = self.patient_database.view_patient_details()
        for data in patient_data:
            for age in range(min_age, max_age+1):
                if data[3] == age:
                    return
        else:
            raise CustomExceptions.PatientAgeRangeNotFound(min_age,max_age)
        
    def check_patient_id(self,patient_id):
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
        for patient_data in consolidated_patient_ids:
            if patient_data[0] == int(patient_id):
                return
        raise CustomExceptions.PatientIDNotFoundError(patient_id)

    def check_doctor_id(self,doctor_id):
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
        for doctor_data in consolidated_doctor_ids:
            if doctor_data[0] == int(doctor_id):
                return
        raise CustomExceptions.DoctorIDNotFoundError(doctor_id)

    def check_doctor_name(self,doctor_name):
        """
        Checks if the doctor name:
        1. Exists in the database
        2. Is entered by the user
        3. Contains only alphabets
        """
        doctor_name_without_spaces = ''.join(doctor_name.split())
        if not doctor_name_without_spaces:
            raise CustomExceptions.InputNotFoundError()
    
        if not doctor_name_without_spaces:
            raise CustomExceptions.InvalidInputDataError(doctor_name)
            
        consolidated_doctor_name = HospitalDatabase.DoctorTable().view_doctor_details()
        for doctor_data in consolidated_doctor_name:
            if doctor_data[1] == doctor_name.strip():
                return
        raise CustomExceptions.DoctorNameNotFoundError(doctor_name)
    
    def add_patient(self):
        """
        Add a new patient to the database. This function will create a new patient ID and insert the patient data into the database.
        Getting the patient's name by checking if the input is valid. 
        If the input is invalid even after 5 tries, the input is completely discarded
        """
        try:
            patient_name = utility.get_input_with_retry(
                "Patient's Name: ",
                self.check_patient_name_or_disease,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if patient_name is None:
                return
                
            ''' 
            Getting the patient's age by checking if the input is valid. 
            If the input is invalid even after 5 tries, the input is completely discarded
            '''
            patient_age = utility.get_input_with_retry(
                "Patient's Age: ",
                self.check_patient_age,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError)
            )
            if patient_age is None:
                return
            
            ''' 
            Getting the patient's disease by checking if the input is valid. 
            If the input is invalid even after 5 tries, the input is completely discarded
            '''
            patient_disease = utility.get_input_with_retry(
                "Patient's Disease: ",
                self.check_patient_name_or_disease,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if patient_disease is None:
                return

            self.patient_database.insert_patient(patient_name, int(patient_age), patient_disease)
            print("Patient Added Successfully!")
            self.hospital_logger.info(f"Patient Name:{patient_name}, Patient Age:{patient_age}, Disease: {patient_disease} added into Patient Table")
        except Exception as e:
            print(f"Error: {e}")

    def view_patient_details(self):
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

    def delete_patient_details(self):
        """
        Delete a patient's details from the database based on the patient ID. 
        This function will prompt the user to enter a patient ID and delete the corresponding patient data from the database.
        """
        try:
            patient_id = utility.get_input_with_retry(
                "Enter Patient ID to delete: ",
                self.check_patient_id,
                (CustomExceptions.InputNotFoundError, 
                 CustomExceptions.InvalidPatientIDError,
                 CustomExceptions.PatientIDNotFoundError)
            )
            if patient_id is None:
                return

            self.patient_database.delete_patient_data(int(patient_id))
            print("Patient Deleted Successfully!")
            self.hospital_logger.info(f"Patient ID:{patient_id} is deleted")

        except Exception as e:
            print(f"Error: {e}")
    
    def search_for_patient_by_id(self):
        """
        Searches patient data by the ID entered
        If the ID is not found, an error message is displayed.
        """
        try:
            patient_id = utility.get_input_with_retry(
                "Enter Patient ID to search: ",
                self.check_patient_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidPatientIDError,
                 CustomExceptions.PatientIDNotFoundError)
            )
            if patient_id is None:
                return

            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            self._display_patient(patient_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
    def search_for_patient_by_name(self):
        """
        Searches patient data by the name entered. If many matching data are found, all of them are displayed
        If the name is not found, an error message is displayed.
        """
        try:
            patient_name = utility.get_input_with_retry(
                "Patient Name: ",
                self.check_patient_name_or_disease,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if patient_name is None:
                return

            self.check_if_patient_name_exists(patient_name)
            patient_details = self.patient_database.get_patient_data_by_name(patient_name)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)

        except CustomExceptions.PatientNameNotFoundError as e:
            print(f"Error: {e}")
        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def search_for_patient_by_disease(self):
        """
        Searches patient data by the disease entered. If many matching data are found, all of them are displayed
        If the disease is not found, an error message is displayed.
        """
        try:
            patient_disease = utility.get_input_with_retry(
                "Patient Disease:",
                self.check_patient_name_or_disease,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if patient_disease is None:
                return

            self.check_if_patient_disease_exists(patient_disease)
            patient_details = self.patient_database.get_patient_data_by_disease(patient_disease)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)
        
        except CustomExceptions.PatientDiseaseNotFoundError as e:
            print(f"Error: {e}")
        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
    def search_for_patient_by_agerange(self):
        """
        Searches patient data by the age range entered. If many matching data are found, all of them are displayed
        If the age range is not found, an error message is displayed.
        """
        try:
            min_age = utility.get_input_with_retry(
                "Minimum Age:",
                self.check_patient_age,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError, )
            )
            if min_age is None:
                return
            
            max_age = utility.get_input_with_retry(
                "Maximum Age:",
                self.check_patient_age,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError, )
            )
            if max_age is None:
                return
            
            MIN_AGE, MAX_AGE = int(min_age), int(max_age)
            self.check_if_patient_agerange_exists(MIN_AGE, MAX_AGE)
            patient_details = self.patient_database.get_patient_data_by_age_range(MIN_AGE, MAX_AGE)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)

        except CustomExceptions.PatientAgeRangeNotFound as e:
            print(f'Error: {e}')
        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except CustomExceptions.InvalidMinAgeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def search_for_patient_by_doctor(self):
        """
        Searches patient data by the doctor_id entered. If many matching data are found, all of them are displayed
        If the doctor id is not found, an error message is displayed.
        """
        try:
            doctor_id = utility.get_input_with_retry(
                "Doctor ID:",
                self.check_doctor_id,
                (CustomExceptions.InputNotFoundError, 
                CustomExceptions.DoctorIDNotFoundError, 
                CustomExceptions.InvalidDoctorIDError)
            )
            if doctor_id is None:
                return

            self.check_if_assigned_doctor_id_exists(int(doctor_id))
            patient_details = self.patient_database.get_patient_data_by_doctor(doctor_id)
            
            for patient_data in patient_details:
                self._display_patient(patient_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except CustomExceptions.DoctorIDNotFoundInPatientDatabaseError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def update_patient_name(self):
        """
        Updates the patient name by the patient id entered
        """
        try:
            patient_id = utility.get_input_with_retry(
                "Patient ID: ",
                self.check_patient_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidPatientIDError,
                 CustomExceptions.PatientIDNotFoundError)
            )
            if patient_id is None:
                return

            patient_name = utility.get_input_with_retry(
                "Patient Name: ",
                self.check_patient_name_or_disease,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if patient_name is None:
                return

            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            if patient_data[2] == patient_name.strip():
                print("Patient name matches. No changes made.")
                return

            self.patient_database.update_patient_details(int(patient_id), patient_name.strip(), 'name')
            print("Patient name updated successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id}'s name changed to {patient_name}")

        except Exception as e:
            print(f"Error: {e}")
        
    def update_patient_age(self):
        """
        Updates the patient details by the patient id entered
        """
        try:
            patient_id = utility.get_input_with_retry(
                "Patient ID: ",
                self.check_patient_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidPatientIDError, 
                 CustomExceptions.PatientIDNotFoundError)
            )
            if patient_id is None:
                return

            patient_age = utility.get_input_with_retry(
                "Patient Age: ",
                self.check_patient_age,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError)
            )
            if patient_age is None:
                return

            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            if patient_data[3] == int(patient_age):
                print("Patient age matches. No changes made.")
                return

            self.patient_database.update_patient_details(int(patient_id), int(patient_age), 'age')
            print("Patient age updated successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id}'s age changed to {patient_age}")

        except Exception as e:
            print(f"Error: {e}")

    def update_patient_disease(self):
        """
        Updates the patient disease by the patient id entered
        """
        try:
            patient_id = utility.get_input_with_retry(
                "Patient ID: ",
                self.check_patient_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidPatientIDError,
                 CustomExceptions.PatientIDNotFoundError)
            )
            if patient_id is None:
                return

            patient_disease = utility.get_input_with_retry(
                "Patient Disease: ",
                self.check_patient_name_or_disease,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if patient_disease is None:
                return

            patient_data = self.patient_database.get_patient_data_by_patientid(int(patient_id))
            if patient_data[4] == patient_disease.strip():
                print("Patient disease matches. No changes made.")
                return

            self.patient_database.update_patient_details(int(patient_id), patient_disease.strip(), 'disease')
            print("Patient disease updated successfully!")
            self.hospital_logger.info(f"Patient ID: {patient_id}'s disease changed to {patient_disease}")

        except Exception as e:
            print(f"Error: {e}")
        
    def patient_count_per_doctor(self):
        """
        Displays the patient count of a doctor by doctor id
        """
        try:
            doctor_id = utility.get_input_with_retry(
                    "Doctor ID:",
                    self.check_doctor_id,
                    (CustomExceptions.InputNotFoundError, 
                    CustomExceptions.DoctorIDNotFoundError, 
                    CustomExceptions.InvalidDoctorIDError)
                )
            if doctor_id is None:
                return

            patient_count = self.patient_database.patient_per_doctor_count(doctor_id)
            print(f"Number of patients: {patient_count[0]}")

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except CustomExceptions.DoctorIDNotFoundInPatientDatabaseError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def most_common_disease(self):
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
    
    def most_common_age(self):
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

    def assign_doctor(self):
        """
        Assign a doctor to a patient.

        *args:
            patient_id: ID of the patient
            doctor_name: Name of the doctor to assign

        If multiple doctors share the same name, all are displayed with their details.
        User selects the correct doctor by ID.
        """    
        try:
            patient_id = utility.get_input_with_retry(
                "Patient ID: ",
                self.check_patient_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidPatientIDError,
                 CustomExceptions.PatientIDNotFoundError)
            )
            if patient_id is None:
                return

            doctor_name = utility.get_input_with_retry(
                "Doctor Name: ",
                self.check_doctor_name,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidInputDataError,
                 CustomExceptions.DoctorNameNotFoundError)
            )
            if doctor_name is None:
                return
            
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

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")   

    def _display_patient(self, patient_data):
        """Helper to display patient details"""
        print(f"Patient ID: {patient_data[0]}, "
              f"Patient Name: {patient_data[2]}, "
              f"Patient Age: {patient_data[3]}, "
              f"Patient Disease: {patient_data[4]}, "
              f"Assigned Doctor ID: {patient_data[1]}")