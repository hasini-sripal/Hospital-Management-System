"""
Module for one-time migration script to import existing patients.csv data (from Task 1) into SQLite
"""

from HospitalDatabase import PatientTable, DoctorTable
import csv

def migration() -> None:
    patient_db = PatientTable()
    doctor_db = DoctorTable()
    
    try:
        with open('../Task 1/patient_details.csv', 'r', newline='') as patient_file:
            patient_reader = csv.reader(patient_file)
            patient_db.create_patient_table()
            doctor_db.create_doctor_table()
            count = 0
            
            for patient_data in patient_reader:
                patient_name = patient_data[1]
                patient_age = int(patient_data[2])
                patient_disease = patient_data[3]
                
                patient_db.insert_patient(patient_name, patient_age, patient_disease)
                count += 1
                print(f"Imported: {patient_name}")
        
        print(f"\nAdded {count} patients successfully")
    
    except FileNotFoundError:
        print("Error: patient_details.csv file not found")
    except IndexError:
        print("Error: CSV file has missing columns")
    except ValueError as e:
        print(f"Error: Invalid data format - {e}")
    except Exception as e:
        print(f'Error: {e}')