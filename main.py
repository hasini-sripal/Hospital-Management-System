"""
Main Program for Hospital Management System
"""
from models import Hospital
from HospitalDatabase import PatientTable, DoctorTable

if __name__ == '__main__':
    PatientTable().create_patient_table()
    DoctorTable().create_doctor_table()
    Hospital().run_menu()