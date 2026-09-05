"""
Module that handles front end operations of Hospital Management System.
"""
import Patient, Doctor, CustomExceptions, HospitalDatabase, reports, utility


class Hospital:
    def __init__(self) -> None:
        self.patient = Patient.Patient()
        self.doctor = Doctor.Doctor()
        self.separator = '*'*20

    def menu_patient(self) -> None:
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
                            
                            patient_name = utility.get_input_with_retry(
                            "Patient's Name: ",
                            self.patient.check_patient_name_or_disease,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                            )
                            if patient_name is None:
                                continue
                                            
                            ''' 
                            Getting the patient's age by checking if the input is valid. 
                            If the input is invalid even after 5 tries, the input is completely discarded
                            '''
                            patient_age = utility.get_input_with_retry(
                            "Patient's Age: ",
                            self.patient.check_patient_age,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError)
                            )
                            if patient_age is None:
                                continue
                            
                            ''' 
                            Getting the patient's disease by checking if the input is valid. 
                            If the input is invalid even after 5 tries, the input is completely discarded
                            '''
                            patient_disease = utility.get_input_with_retry(
                            "Patient's Disease: ",
                            self.patient.check_patient_name_or_disease,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                            )
                            
                            if patient_disease is None:
                                continue
                            
                            self.patient.add_patient(patient_name,int(patient_age),patient_disease)
                    else:
                        print("Number of patients field is empty")
                except ValueError:
                    print("Number of patients much be an integer")
                except Exception as e:
                    print(f"Error:{e}")
            
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
                    try:
                        patient_id = utility.get_input_with_retry(
                        "Patient ID: ",
                        self.patient.check_patient_id,
                        (CustomExceptions.InputNotFoundError,
                        CustomExceptions.InvalidPatientIDError,
                        CustomExceptions.PatientIDNotFoundError)
                        )
                        if patient_id is None:
                            continue
                        self.patient.search_for_patient_by_id(int(patient_id))
                    except CustomExceptions.RecordNotFoundError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Error: {e}")

                #Searching for patient by name
                elif choice_without_space == '2':
                    try:
                        patient_name = utility.get_input_with_retry(
                        "Patient Name: ",
                        self.patient.check_patient_name_or_disease,
                        (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        ).strip()
                        if patient_name is None:
                            continue
                    
                        self.patient.check_if_patient_name_exists(patient_name)        
                        self.patient.search_for_patient_by_name(patient_name)

                    except CustomExceptions.PatientNameNotFoundError as e:
                        print(f"Error: {e}")
                    except CustomExceptions.RecordNotFoundError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Error: {e}")

                #Searching for patient by disease
                elif choice_without_space == '3':
                    try:
                        patient_disease = utility.get_input_with_retry(
                        "Patient Disease:",
                        self.check_patient_name_or_disease,
                        (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        ).strip()
                        if patient_disease is None:
                            continue
                    
                        self.patient.check_if_patient_disease_exists(patient_disease)
                        self.patient.search_for_patient_by_disease(patient_disease)
                    except CustomExceptions.PatientDiseaseNotFoundError as e:
                            print(f"Error: {e}")
                    except CustomExceptions.RecordNotFoundError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Error: {e}")
                         
                #Searching for patient by age range
                elif choice_without_space == '4':
                    try:
                        min_age = utility.get_input_with_retry(
                            "Minimum Age:",
                            self.patient.check_patient_age,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError, )
                        )
                        if min_age is None:
                            continue
                        
                        max_age = utility.get_input_with_retry(
                            "Maximum Age:",
                            self.patient.check_patient_age,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError, )
                        )
                        if max_age is None:
                            continue
                        
                        MIN_AGE, MAX_AGE = int(min_age), int(max_age)
                        self.patient.check_if_patient_agerange_exists(MIN_AGE, MAX_AGE)
                        self.patient.search_for_patient_by_agerange(MIN_AGE, MAX_AGE)
                    except CustomExceptions.PatientAgeRangeNotFound as e:
                        print(f'Error: {e}')
                    except CustomExceptions.RecordNotFoundError as e:
                        print(f"Error: {e}")
                    except CustomExceptions.InvalidMinAgeError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Error: {e}")

                #Searching for patient by assigned doctor_id
                elif choice_without_space == '5':
                    try:
                        doctor_id = utility.get_input_with_retry(
                            "Doctor ID:",
                            self.patient.check_doctor_id,
                            (CustomExceptions.InputNotFoundError, 
                            CustomExceptions.DoctorIDNotFoundError, 
                            CustomExceptions.InvalidDoctorIDError)
                        )
                        if doctor_id is None:
                            continue
                        self.patient.search_for_patient_by_doctor(int(doctor_id))
                    except CustomExceptions.RecordNotFoundError as e:
                        print(f"Error: {e}")
                    except CustomExceptions.DoctorIDNotFoundInPatientDatabaseError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Error: {e}")
            
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
                    try:
                        patient_id = utility.get_input_with_retry(
                            "Patient ID: ",
                            self.patient.check_patient_id,
                            (CustomExceptions.InputNotFoundError,
                            CustomExceptions.InvalidPatientIDError,
                            CustomExceptions.PatientIDNotFoundError)
                        )
                        if patient_id is None:
                            continue
            
                        patient_name = utility.get_input_with_retry(
                            "Patient Name: ",
                            self.patient.check_patient_name_or_disease,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        )
                        if patient_name is None:
                            continue

                        self.patient.update_patient_name(int(patient_id),patient_name)

                    except Exception as e:
                                print(f"Error: {e}")

                #Updating Patient's age
                elif choice_without_space == '2':
                    try:
                        patient_id = utility.get_input_with_retry(
                            "Patient ID: ",
                            self.patient.check_patient_id,
                            (CustomExceptions.InputNotFoundError,
                             CustomExceptions.InvalidPatientIDError, 
                             CustomExceptions.PatientIDNotFoundError)
                        )
                        if patient_id is None:
                            continue
            
                        patient_age = utility.get_input_with_retry(
                            "Patient Age: ",
                            self.patient.check_patient_age,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidAgeError)
                        )
                        if patient_age is None:
                            continue
                        self.patient.update_patient_age(int(patient_id),patient_age)
                    except Exception as e:
                        print(f"Error: {e}")

                #Updating Patient's disease
                elif choice_without_space == '3':
                    try:
                        patient_id = utility.get_input_with_retry(
                            "Patient ID: ",
                            self.check_patient_id,
                            (CustomExceptions.InputNotFoundError,
                             CustomExceptions.InvalidPatientIDError,
                             CustomExceptions.PatientIDNotFoundError)
                        )
                        if patient_id is None:
                            continue
            
                        patient_disease = utility.get_input_with_retry(
                            "Patient Disease: ",
                            self.check_patient_name_or_disease,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        )
                        if patient_disease is None:
                            continue

                        self.patient.update_patient_disease(int(patient_id), patient_disease)

                    except Exception as e:
                        print(f"Error: {e}")
            
                elif choice_without_space.lower() == 'q':
                    pass

                else:
                    print("Invalid choice. Please Try Again!")

    #Option 5 deletes the patient details on the basis of patient id
            elif ans_without_space == '5':
                try:
                    patient_id = utility.get_input_with_retry(
                    "Enter Patient ID to delete: ",
                    self.patient.check_patient_id,
                    (CustomExceptions.InputNotFoundError, 
                    CustomExceptions.InvalidPatientIDError,
                    CustomExceptions.PatientIDNotFoundError)
                    )
                    if patient_id is None:
                        continue
                    self.patient.delete_patient_details(int(patient_id))
                except Exception as e:
                    print(f"Error:{e}")

    #Option 6 assigns a doctor to the patient
            elif ans_without_space == '6':
                try:
                    #Number of patients to be assigned to doctor
                    patient_count = int(input("Enter the number of patients to be assigned:"))
                    #Checking if the input is entered by the user
                    if patient_count:
                        for trial in range(1, patient_count+1):
                            print(f"Patient No. : {trial}")
                            patient_id = utility.get_input_with_retry(
                            "Patient ID: ",
                            self.patient.check_patient_id,
                            (CustomExceptions.InputNotFoundError,
                            CustomExceptions.InvalidPatientIDError,
                            CustomExceptions.PatientIDNotFoundError)
                            )
                            if patient_id is None:
                                continue
                            
                            doctor_name = utility.get_input_with_retry(
                            "Doctor Name: ",
                            self.patient.check_doctor_name,
                            (CustomExceptions.InputNotFoundError,
                            CustomExceptions.InvalidInputDataError,
                            CustomExceptions.DoctorNameNotFoundError)
                            )
                            if doctor_name is None:
                                continue
                            self.patient.assign_doctor(patient_id,doctor_name)

                except CustomExceptions.RecordNotFoundError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error: {e}")

            elif ans_without_space.lower() == 'q':
                print(f"{self.separator}END OF OPERATIONS{self.separator}")
                break
            
            else:
                print("INVALID OPTION. TRY AGAIN")        
        print('\n')                                 #for legibility
    
    def menu_doctor(self) -> None:
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
                            doctor_name = utility.get_input_with_retry(
                                "Doctor's Name: ",
                                self.doctor.check_doctor_name_or_specialization,
                                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                            )
                            if doctor_name is None:
                                continue
                
                            doctor_name = doctor_name.strip()
                
                            doctor_specialisation = utility.get_input_with_retry(
                                "Doctor's Specialisation: ",
                                self.doctor.check_doctor_name_or_specialization,
                                (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                            )
                            if doctor_specialisation is None:
                                continue
                            doctor_specialisation = doctor_specialisation.strip()
                            
                            self.doctor.add_doctor(doctor_name, doctor_specialisation)
                    else:
                        print("Number of doctors field is empty")
                except ValueError:
                    print("Number of doctors much be an integer")
                except Exception as e:
                    print(f"Error: {e}")

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
                    try:
                        doctor_id = utility.get_input_with_retry(
                            "Enter Doctor ID to search: ",
                            self.check_doctor_id,
                            (CustomExceptions.InputNotFoundError,
                             CustomExceptions.InvalidDoctorIDError,
                             CustomExceptions.DoctorIDNotFoundError)
                        )
                        if doctor_id is None:
                            continue
                        self.doctor.search_for_doctor_by_id(int(doctor_id))
                    except Exception as e:
                        print(f"Error: {e}")

                #Searching for doctor by name
                elif choice_without_space == '2':
                    try:
                        doctor_name = utility.get_input_with_retry(
                            "Enter Doctor Name to search: ",
                            self.doctor.check_doctor_name_or_specialization,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        ).strip()
                        if doctor_name is None:
                            continue
            
                        self.doctor.check_if_doctor_name_exists(doctor_name)
                        self.doctor.search_for_doctor_by_name(doctor_name)

                    except Exception as e:
                        print(f"Error: {e}")
                        
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
                    try:
                        doctor_id = utility.get_input_with_retry(
                            "Doctor ID: ",
                            self.doctor.check_doctor_id,
                            (CustomExceptions.InputNotFoundError,
                             CustomExceptions.InvalidDoctorIDError,
                             CustomExceptions.DoctorIDNotFoundError)
                        )
                        if doctor_id is None:
                            continue
            
                        doctor_name = utility.get_input_with_retry(
                            "Doctor's Name: ",
                            self.doctor.check_doctor_name_or_specialization,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        )
                        if doctor_name is None:
                            continue
                        self.doctor.update_doctor_name(int(doctor_id),doctor_name)
                    except Exception as e:
                        print(f'Error: {e}')

                #Updating Doctor's specialisation
                elif choice_without_space == '2':
                    try:
                        doctor_id = utility.get_input_with_retry(
                            "Doctor ID: ",
                            self.doctor.check_doctor_id,
                            (CustomExceptions.InputNotFoundError,
                             CustomExceptions.InvalidDoctorIDError,
                             CustomExceptions.DoctorIDNotFoundError)
                        )
                        if doctor_id is None:
                            continue
            
                        doctor_specialisation = utility.get_input_with_retry(
                            "Doctor's Specialisation: ",
                            self.doctor.check_doctor_name_or_specialization,
                            (CustomExceptions.InputNotFoundError, CustomExceptions.InvalidInputDataError)
                        )
                        if doctor_specialisation is None:
                            continue
            
                        self.doctor.update_doctor_specialisation(int(doctor_id), doctor_specialisation)
                    except Exception as e:
                        print(f"Error :{e}")
                elif choice_without_space.lower() == 'q':
                    pass
                else:
                    print("Invalid choice. Please Try Again!")

            #Option 5 deletes the doctor details on the basis of doctor id
            elif ans_without_space == '5':
                try:
                    doctor_id = utility.get_input_with_retry(
                    "Enter Doctor ID to delete: ",
                    self.doctor.check_doctor_id,
                    (CustomExceptions.InputNotFoundError,
                    CustomExceptions.InvalidDoctorIDError,
                    CustomExceptions.DoctorIDNotFoundError)
                    )
                    if doctor_id is None:
                        continue
                    self.doctor.delete_doctor_details(int(doctor_id))
                except Exception as e:
                    print(f'Error: {e}')
            
            elif ans_without_space.lower() == 'q':
                print(f"{self.separator}END OF OPERATIONS{self.separator}")
                break
            
            else:
                print("INVALID OPTION. TRY AGAIN")
        print('\n')                                     #for legibility
        
    def simple_report(self) -> None:
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
                try:
                        doctor_id = utility.get_input_with_retry(
                        "Doctor ID:",
                        self.patient.check_doctor_id,
                        (CustomExceptions.InputNotFoundError, 
                        CustomExceptions.DoctorIDNotFoundError, 
                        CustomExceptions.InvalidDoctorIDError)
                        )
                        if doctor_id is None:
                            continue
                        self.patient.patient_count_per_doctor(int(doctor_id))
                except CustomExceptions.RecordNotFoundError as e:
                    print(f"Error: {e}")
                except CustomExceptions.DoctorIDNotFoundInPatientDatabaseError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error: {e}")

            elif ans_without_space == '2':
                self.patient.most_common_disease()
            elif ans_without_space == '3':
                self.patient.most_common_age()
            elif ans_without_space == 'q':
                print(f"{self.separator}END OF OPERATIONS{self.separator}")
                break
            else:
                print("INVALID OPTION. TRY AGAIN")

    def generate_excel_report(self) -> None:
        reports.generate_patient_report()
        reports.generate_doctor_report()
        reports.generate_summary_report()
        print("Report Generated")

    def run_menu(self) -> None:
        while True:
            options = input("""Options
1. Patient Management System
2. Doctor Management System
3. Simple Report
4. Excel Report
Enter one of the options or 'q' to quit: """)
            
            options_without_space = options.strip()     #removing trailing and leading white spaces
            if options_without_space == '1':
                self.menu_patient()
            elif options_without_space == '2':
                self.menu_doctor()
            elif options_without_space == '3':
                self.simple_report()
            elif options_without_space == '4':
                self.generate_excel_report()
            elif options_without_space == 'q':
                print(f"{self.separator}END OF OPERATION{self.separator}")
                break
            else:
                print("INVALID OPTION. TRY AGAIN")
            print('\n')                                     #for legibility
