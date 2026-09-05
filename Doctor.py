"""
Module that handles Doctor Management System
"""

import config_loader, logger, utility, CustomExceptions, HospitalDatabase
from datetime import datetime

class Doctor:
    def __init__(self) -> None:
        self.doctor_database = HospitalDatabase.DoctorTable()
        config = config_loader.load_config('config.json')
        self.MAX_TRIES = config.get("max_input_tries", 5)
        self.hospital_logger = logger.get_logger()
        self.doctor_id = None
        self.doctor_name = None
        self.doctor_specialisation = None
        self.created_at = None

    def __str__(self) -> str:
        """
        String representation of the Doctor class. Returns the doctor name and specialization.
        """
        return f"Doctor [{self.doctor_id}: {self.doctor_name}], Doctor Specialization: {self.doctor_specialisation}"

    def __repr__(self) -> str:
        """
        Representation of the Doctor class. Returns the doctor id, name, and specialization.
        """
        return (f"Doctor(id={self.doctor_id}, name={self.doctor_name!r}," 
                f"specialisation={self.doctor_specialisation!r})")
    
    def check_doctor_name_or_specialization(self, doctor_data: str) -> None:
        """
        Checks if the doctor name or specialization:
        1. is entered by the user
        2. contains only alphabets and spaces
        """
        doctor_data = doctor_data.strip()
        if not doctor_data:
            raise CustomExceptions.InputNotFoundError()
        if not all(c.isalpha() or c.isspace() or c in "'-" for c in doctor_data):
            raise CustomExceptions.InvalidInputDataError(doctor_data)
        
    def check_doctor_id(self, doctor_id:str) -> None:
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
            
        consolidated_doctor_ids = self.doctor_database.view_doctor_details()
        if any(doctor_data[0] == int(doctor_id) for doctor_data in consolidated_doctor_ids):
            return
        raise CustomExceptions.DoctorIDNotFoundError(doctor_id)
    
    def check_if_doctor_name_exists(self, doctor_name:str) -> None:
        """
        Checks if the doctor's name exists in the database
        """
        doctor_data = self.doctor_database.view_doctor_details()
        if any(name[1] == doctor_name.strip() for name in doctor_data):
            return
        raise CustomExceptions.DoctorNameNotFoundError(doctor_name)            

    def check_no_of_patients(self,no_of_patients:str) -> None:
        """
        Checks if the number of patients handled by the doctor:
        1. is entered by the user
        2. contains only numbers
        """
        if not no_of_patients.strip():
            raise CustomExceptions.InputNotFoundError()
        if not no_of_patients.isdigit():
            raise CustomExceptions.InvalidPatientCountError(no_of_patients)

    @utility.log_action   
    def add_doctor(self, doctor_name:str, doctor_specialisation:str) -> None:
        """
        Add a new doctor to the database. This function will create a new doctor ID and insert the doctor data into the database.
        """
        try:
            self.doctor_name, self.doctor_specialisation = doctor_name, doctor_specialisation
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.doctor_database.insert_doctor(self.doctor_name, self.doctor_specialisation, self.created_at)
            print("Doctor added successfully!")
            self.hospital_logger.info(f"Doctor Name:{self.doctor_name}, Specialisation:{self.doctor_specialisation} is added into the doctor table")

            self.doctor_id = self.doctor_database.get_last_inserted_doctor_id()

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action
    @utility.timer
    def view_doctor_details(self) -> None:
        """
        Function to view all the doctor details from the database.
        """
        try:
            doctor_details = self.doctor_database.view_doctor_details()
            for doctor_data in doctor_details:
                self._display_doctor(doctor_data)

            NO_OF_DOCTORS = len(doctor_details)
            print(f"Number of doctors: {NO_OF_DOCTORS}")              
        
        except CustomExceptions.RecordNotFoundError as e:
            print (f"Error: {e}")
        except Exception as e:
            print (f"Error: {e}")

    @utility.log_action 
    def delete_doctor_details(self, doctor_id: int) -> None:
        """
        Delete a doctor's details from the database based on the doctor ID. 
        This function will prompt the user to enter a doctor ID and delete the corresponding doctor data from the database.
        """
        try:
            self.doctor_database.delete_doctor_data(int(doctor_id))
            print("Doctor deleted successfully!")
            self.hospital_logger.info(f"Doctor ID:{doctor_id} is deleted")

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def search_for_doctor_by_id(self, doctor_id:int) -> None:
        """
        Searches the doctor data by the id entered.
        If the ID not found, an error message is displayed.
        """
        try:
            doctor_data = self.doctor_database.get_doctor_data_by_doctorid(int(doctor_id))
            self._display_doctor(doctor_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action   
    def search_for_doctor_by_name(self, doctor_name: str) -> None:
        """
        Searches the doctor details by the name entered. If many matching data are found, all of them are displayed
        If the name is not found, an error message is displayed.
        """
        try:
            doctor_details = self.doctor_database.get_doctor_data_by_name(doctor_name.strip())
            
            for doctor_data in doctor_details:
                self._display_doctor(doctor_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    @utility.log_action
    def update_doctor_name(self, doctor_id:int, doctor_name:str)-> None:
        """
        Updates the doctor name by the doctor id entered.
        If the data matches, then no changes take place and user is known that the data matches
        """
        try:
            doctor_data = self.doctor_database.get_doctor_data_by_doctorid(doctor_id)
            if doctor_data[1] == doctor_name.strip():
                print("Doctor name matches. No changes made.")
                return

            self.doctor_database.update_doctor_data(int(doctor_id), doctor_name.strip(), 'name')
            print("Doctor name updated successfully!")
            self.hospital_logger.info(f"Doctor ID: {doctor_id}'s name changed to {doctor_name}")

        except Exception as e:
            print(f"Error: {e}")

    @utility.log_action 
    def update_doctor_specialisation(self, doctor_id:int, doctor_specialisation:str) -> None:
        """
        Updates the doctor's specialisation by the doctor id entered by the user
        If the data matches, then no changes take place and user is known that the data matches
        """
        try:
            doctor_data = self.doctor_database.get_doctor_data_by_doctorid(int(doctor_id))
            if doctor_data[2] == doctor_specialisation.strip():
                print("Doctor specialisation matches. No changes made.")
                return

            self.doctor_database.update_doctor_data(int(doctor_id), doctor_specialisation.strip(), 'specialisation')
            print("Doctor specialisation updated successfully!")
            self.hospital_logger.info(f"Doctor ID: {doctor_id}'s specialisation changed to {doctor_specialisation}")

        except Exception as e:
            print(f"Error: {e}")

         
    def _display_doctor(self, doctor_data:tuple) -> None:
        """Helper to display doctor details"""
        print(f"Doctor ID: {doctor_data[0]}, "
              f"Doctor Name: {doctor_data[1]}, "
              f"Doctor Specialization: {doctor_data[2]}, "
              f"Time of Admission: {doctor_data[3]}")
