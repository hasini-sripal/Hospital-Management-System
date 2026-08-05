"""
Module that handles Doctor Management System
"""

import HospitalDatabase
import CustomExceptions
import utility
import logger

class Doctor:
    def __init__(self):
        self.doctor_database = HospitalDatabase.DoctorTable()
        self.MAX_TRIES = 5
        self.hospital_logger = logger.get_logger()
    
    def check_doctor_name_or_specialization(self, doctor_data):
        """
        Checks if the doctor name or specialization:
        1. is entered by the user
        2. contains only alphabets
        """
        doctor_data_without_spaces = ''.join(doctor_data.split())
        if not doctor_data_without_spaces.strip():
            raise CustomExceptions.InputNotFoundError()
        if not doctor_data_without_spaces.isalpha():
            raise CustomExceptions.InvalidInputDataError(doctor_data)
        
    def check_doctor_id(self, doctor_id):
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
        for doctor_data in consolidated_doctor_ids:
            if doctor_data[0] == int(doctor_id):
                return
        raise CustomExceptions.DoctorIDNotFoundError(doctor_id)
    
    def check_if_doctor_name_exists(self, doctor_name):
        """
        Checks if the doctor's name exists in the database
        """
        doctor_data = self.doctor_database.get_all_doctors()
        for name in doctor_data:
            if name[1] == doctor_name.strip():
                return
        else:
            raise CustomExceptions.DoctorNameNotFoundError(doctor_name)            

    def check_no_of_patients(self,no_of_patients):
        """
        Checks if the number of patients handled by the doctor:
        1. is entered by the user
        2. contains only numbers
        """
        if not no_of_patients.strip():
            raise CustomExceptions.InputNotFoundError()
        if not no_of_patients.isdigit():
            raise CustomExceptions.InvalidAgeError(no_of_patients)
        
    def add_doctor(self):
        """
        Add a new doctor to the database. This function will create a new doctor ID and insert the doctor data into the database.
        """
        try:
            doctor_name = utility.get_input_with_retry(
                "Doctor's Name: ",
                self.check_doctor_name_or_specialization,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if doctor_name is None:
                return

            doctor_specialisation = utility.get_input_with_retry(
                "Doctor's Specialisation: ",
                self.check_doctor_name_or_specialization,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if doctor_specialisation is None:
                return

            self.doctor_database.insert_doctor(doctor_name, doctor_specialisation)
            print("Doctor added successfully!")
            self.hospital_logger.info(f"Doctor Name:{doctor_name}, Specialisation:{doctor_specialisation} is added into the doctor table")

        except Exception as e:
            print(f"Error: {e}")
    
    def view_doctor_details(self):
        """
        Function to view all the doctor details from the database.
        """
        try:
            doctor_details = self.doctor_database.view_doctor_details()
            for doctor_data in doctor_details:
                self._display_doctor(doctor_data)               
        
        except CustomExceptions.RecordNotFoundError as e:
            print (f"Error: {e}")
        except Exception as e:
            print (f"Error: {e}")
        
    def delete_doctor_details(self):
        """
        Delete a doctor's details from the database based on the doctor ID. 
        This function will prompt the user to enter a doctor ID and delete the corresponding doctor data from the database.
        """
        try:
            doctor_id = utility.get_input_with_retry(
                "Enter Doctor ID to delete: ",
                self.check_doctor_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidDoctorIDError,
                 CustomExceptions.DoctorIDNotFoundError)
            )
            if doctor_id is None:
                return

            self.doctor_database.delete_doctor_data(int(doctor_id))
            print("Doctor deleted successfully!")
            self.hospital_logger.info(f"Doctor ID:{doctor_id} is deleted")

        except Exception as e:
            print(f"Error: {e}")
    
    def search_for_doctor_by_id(self):
        """
        Searches the doctor data by the id entered.
        If the ID not found, an error message is displayed.
        """
        try:
            doctor_id = utility.get_input_with_retry(
                "Enter Doctor ID to search: ",
                self.check_doctor_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidDoctorIDError,
                 CustomExceptions.DoctorIDNotFoundError)
            )
            if doctor_id is None:
                return

            doctor_data = self.doctor_database.get_doctor_data_by_doctorid(int(doctor_id))
            self._display_doctor(doctor_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
    def search_for_doctor_by_name(self):
        """
        Searches the doctor details by the name entered. If many matching data are found, all of them are displayed
        If the name is not found, an error message is displayed.
        """
        try:
            doctor_name = utility.get_input_with_retry(
                "Enter Doctor Name to search: ",
                self.check_doctor_name_or_specialization,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if doctor_name is None:
                return

            self.check_if_doctor_name_exists(doctor_name)
            doctor_details = self.doctor_database.get_doctor_data_by_name(doctor_name)
            
            for doctor_data in doctor_details:
                self._display_doctor(doctor_data)

        except CustomExceptions.RecordNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def update_doctor_name(self):
        """
        Updates the doctor name by the doctor id entered.
        If the data matches, then no changes take place and user is known that the data matches
        """
        try:
            doctor_id = utility.get_input_with_retry(
                "Doctor ID: ",
                self.check_doctor_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidDoctorIDError,
                 CustomExceptions.DoctorIDNotFoundError)
            )
            if doctor_id is None:
                return

            doctor_name = utility.get_input_with_retry(
                "Doctor's Name: ",
                self.check_doctor_name_or_specialization,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if doctor_name is None:
                return

            doctor_data = self.doctor_database.get_doctor_data_by_doctorid(int(doctor_id))
            if doctor_data[1] == doctor_name.strip():
                print("Doctor name matches. No changes made.")
                return

            self.doctor_database.update_doctor_data(int(doctor_id), doctor_name.strip(), 'name')
            print("Doctor name updated successfully!")
            self.hospital_logger.info(f"Doctor ID: {doctor_id}'s name changed to {doctor_name}")

        except Exception as e:
            print(f"Error: {e}")
        
    def update_doctor_specialisation(self):
        """
        Updates the doctor's specialisation by the doctor id entered by the user
        If the data matches, then no changes take place and user is known that the data matches
        """
        try:
            doctor_id = utility.get_input_with_retry(
                "Doctor ID: ",
                self.check_doctor_id,
                (CustomExceptions.InputNotFoundError,
                 CustomExceptions.InvalidDoctorIDError,
                 CustomExceptions.DoctorIDNotFoundError)
            )
            if doctor_id is None:
                return

            doctor_specialisation = utility.get_input_with_retry(
                "Doctor's Specialisation: ",
                self.check_doctor_name_or_specialization,
                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
            )
            if doctor_specialisation is None:
                return

            doctor_data = self.doctor_database.get_doctor_data_by_doctorid(int(doctor_id))
            if doctor_data[2] == doctor_specialisation.strip():
                print("Doctor specialisation matches. No changes made.")
                return

            self.doctor_database.update_doctor_data(int(doctor_id), doctor_specialisation.strip(), 'specialisation')
            print("Doctor specialisation updated successfully!")
            self.hospital_logger.info(f"Doctor ID: {doctor_id}'s specialisation changed to {doctor_specialisation}")

        except Exception as e:
            print(f"Error: {e}")
            
    def _display_doctor(self, doctor_data):
        """Helper to display doctor details"""
        print(f"Doctor ID: {doctor_data[0]}, "
              f"Doctor Name: {doctor_data[1]}, "
              f"Doctor Specialization: {doctor_data[2]}")