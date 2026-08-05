"""
Module that handles front end operations of Hospital Management System.
"""
import HospitalDatabase
import CustomExceptions
import Patient
import Doctor


class Hospital:
    def __init__(self):
        self.database = HospitalDatabase
        self.patient = Patient.Patient()
        self.doctor = Doctor.Doctor()
        self.separator = '*'*20

    def menu_patient(self):
        """
        Function that acts as a menu for Patient Management System
        """
        #Showing the patient list before loading
        self.patient.view_patient_details()
        while True:
            ans = input(""" MENU    
1. Add Patient
2. View Details of all the Patients
3. Search for a Patient
4. Update Patient 
5. Delete Patient
6. Assign Doctor
Enter options(1-5) or 'q' to quit: """)
            ans_without_space = ans.strip()
            #Option 1 adds new patient to the database       #removing leading and trailing spaces from the user inputted option
            if ans_without_space == '1':
                try:
                    #Number of patients to be added in the database
                    patient_count = int(input("Enter the number of patients to be added:"))
                    #Checking if the input is entered by the user
                    if patient_count:
                        for trial in range(1, patient_count+1):
                            print(f"Patient No. : {trial}")
                            self.patient.add_patient()
                    else:
                        print("Number of patients field is empty")
                except ValueError:
                    print("Number of patients much be an integer")
            
            #Option 2 allows user to view all the patients' details
            elif ans_without_space == '2':
                self.patient.view_patient_details()
            
            #Option 3 is to search for patients
            elif ans_without_space == '3':
                choice = input(""" Options
1. Search for Patient using Patient ID
2. Search for Patient using Patient Name
3. Search for Patient using Patient Disease
4. Search for Patient using Age Range
5. Search for Patient using Assigned Doctor
Enter one of the options or 'q' to quit: """)
                print('\n')                                 #for legibility
                choice_without_space = choice.strip()       #removing leading and trailing spaces from the user inputted option
                
                #Searching for patient by id
                if choice_without_space == '1':
                    self.patient.search_for_patient_by_id()
                #Searching for patient by name
                elif choice_without_space == '2':
                    self.patient.search_for_patient_by_name()
                #Searching for patient by disease
                elif choice_without_space == '3':
                    self.patient.search_for_patient_by_disease()
                #Searching for patient by age range
                elif choice_without_space == '4':
                    self.patient.search_for_patient_by_agerange()
                #Searching for patient by assigned doctor_id
                elif choice_without_space == '5':
                    self.patient.search_for_patient_by_doctor()
            
                elif choice_without_space.lower() == 'q':
                    pass
                else:
                    print("Invalid choice. Please Try Again!")

            #Option 4 is to update patient details
            elif ans_without_space == '4':
                choice = input(""" Options
1. Update Patient's Name
2. Update Patient's Age
3. Update Patient's Disease
Enter one of the options or 'q' to quit: """)
                print('\n')                                 #for legibility
                choice_without_space = choice.strip()       #removing leading and trailing spaces from the user inputted option
                #Updating Patient's name
                if choice_without_space == '1':
                    self.patient.update_patient_name()
                #Updating Patient's age
                elif choice_without_space == '2':
                    self.patient.update_patient_age()
                #Updating Patient's disease
                elif choice_without_space == '3':
                    self.patient.update_patient_disease()
                elif choice_without_space.lower() == 'q':
                    pass
                else:
                    print("Invalid choice. Please Try Again!")
    #Option 5 deletes the patient details on the basis of patient id
            elif ans_without_space == '5':
                self.patient.delete_patient_details()
    
    #Option 5 assigns a doctor to the patient
            elif ans_without_space == '6':
                #Number of patients to be assigned to doctor
                patient_count = int(input("Enter the number of patients to be assigned:"))
                #Checking if the input is entered by the user
                if patient_count:
                    for trial in range(1, patient_count+1):
                        print(f"Patient No. : {trial}")
                        self.patient.assign_doctor()

            elif ans_without_space.lower() == 'q':
                print(f"{self.separator}END OF OPERATIONS{self.separator}")
                break
            
            else:
                print("INVALID OPTION. TRY AGAIN")        
        print('\n')                                 #for legibility
    
    def menu_doctor(self):
        self.doctor.view_doctor_details()
        while True:
            ans = input(""" MENU    
1. Add Doctor
2. View Details of all the Doctors
3. Search for a Doctor
4. Update Doctor
5. Delete Doctor
Enter options(1-5) or 'q' to quit: """)
            ans_without_space = ans.strip()           #removing leading and trailing spaces from the user inputted option
            #Option 1 adds new doctor to the database       
            if ans_without_space == '1':
                try:
                    #Number of doctors to be added in the database
                    doctor_count = int(input("Enter the number of doctors to be added: "))
                    #Checking if the input is entered by the user
                    if doctor_count:
                        for trial in range(1, doctor_count+1):
                            print(f"Doctor No. : {trial}")
                            self.doctor.add_doctor()
                    else:
                        print("Number of doctors field is empty")
                except ValueError:
                    print("Number of doctors much be an integer")

            #Option 2 allows user to view all the doctors' details
            elif ans_without_space == '2':
                self.doctor.view_doctor_details()
                
            #Option 3 is to search for doctors
            elif ans_without_space == '3':
                choice = input(""" Options
1. Search for Doctor using Doctor ID
2. Search for Doctor using Doctor Name
Enter one of the options or 'q' to quit: """)
                print('\n')                                 #for legibility

                choice_without_space = choice.strip()       #removing leading and trailing spaces from the user inputted option
                #Searching for doctor by id
                if choice_without_space == '1':
                    self.doctor.search_for_doctor_by_id()
                #Searching for doctor by name
                elif choice_without_space == '2':
                    self.doctor.search_for_doctor_by_name()
                elif choice_without_space.lower() == 'q':
                    pass
                else:
                    print("Invalid choice. Please Try Again!")

            #Option 4 is to update doctor details
            elif ans_without_space == '4':
                choice = input(""" Options
1. Update Doctor's Name
2. Update Doctor's Specialisation
Enter one of the options or 'q' to quit: """)
                print('\n')                                 #for legibility

                choice_without_space = choice.strip()       #removing leading and trailing spaces from the user inputted option
                #Updating Doctor's name
                if choice_without_space == '1':
                    self.doctor.update_doctor_name()
                #Updating Doctor's specialisation
                elif choice_without_space == '2':
                    self.doctor.update_doctor_specialisation()
                elif choice_without_space.lower() == 'q':
                    pass
                else:
                    print("Invalid choice. Please Try Again!")

            #Option 5 deletes the doctor details on the basis of doctor id
            elif ans_without_space == '5':
                self.doctor.delete_doctor_details()
            
            elif ans_without_space.lower() == 'q':
                print(f"{self.separator}END OF OPERATIONS{self.separator}")
                break
            
            else:
                print("INVALID OPTION. TRY AGAIN")
        print('\n')                                     #for legibility
        
    def simple_report(self):
        """
        Shows the simple report containing
        1. Patient count per doctor
        2. Most Common Disease
        3. Most Common Age
        """
        while True:
            ans = input("""MENU
1. Patient Count per Doctor
2. Most Common Disease
3. Most Common Age Group
Enter one of the options or 'q' to quit:""")
            ans_without_space = ans.strip()
            if ans_without_space == '1':
                self.patient.patient_count_per_doctor()
            elif ans_without_space == '2':
                self.patient.most_common_disease()
            elif ans_without_space == '3':
                self.patient.most_common_age()
            elif ans_without_space == 'q':
                print(f"{self.separator}END OF OPERATIONS{self.separator}")
                break
            else:
                print("INVALID OPTION. TRY AGAIN")

    def run_menu(self):
        while True:
            options = input("""Options
1. Patient Management System
2. Doctor Management System
3. Simple Report
Enter one of the options or 'q' to quit: """)
            
            options_without_space = options.strip()     #removing trailing and leading white spaces
            if options_without_space == '1':
                self.menu_patient()
            elif options_without_space == '2':
                self.menu_doctor()
            elif options_without_space == '3':
                self.simple_report()
            elif options_without_space == 'q':
                print(f"{self.separator}END OF OPERATION{self.separator}")
                self.patient.patient_database.close_connection()
                self.doctor.doctor_database.close_connection()
                break
            else:
                print("INVALID OPTION. TRY AGAIN")
            print('\n')                                     #for legibility