"""

Controls the Database Management of the Hospital Management System.
Contains:
1. PatientDatabase class
2. DoctorDatabase class

"""
import sqlite3 as sql
import CustomExceptions

class PatientTable:
    '''
    Class that handles the database operations for patients in the Hospital Management System
    '''
    def __init__(self):
        '''
        Constructor for the PatientDatabase class. Initializes the database connection and cursor
        '''
        self.hospital_database = sql.connect('hospital_database.db')
        self.cursor = self.hospital_database.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def create_patient_table(self):
        '''
        Function to create the patients table in the database if it does not already exist
        '''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assigned_doctor_id INTEGER REFERENCES doctors(doctor_id),
            patient_name TEXT NOT NULL,
            patient_age INTEGER NOT NULL,
            patient_disease TEXT NOT NULL
        )''')
        self.hospital_database.commit()

    def insert_patient(self, patient_name, patient_age, patient_disease):
        '''
        Function to insert a new patient into the database
        '''
        self.cursor.execute('''
            INSERT INTO patients (patient_name, patient_age, patient_disease)
            VALUES (?, ?, ?)''', (patient_name, patient_age, patient_disease)
        )
        self.hospital_database.commit()
    
    def update_patient_details(self, patient_id, new_patient_data, field_name):
        """
        Function to update patient data in the database based on the field name provided
        *args field_name: The name of the field to be updated. It can be one of the following:
            - 'name': Updates the patient's name. 
            - 'age': Updates the patient's age.
            - 'disease': Updates the patient's disease.
            - 'doctor': Updates the assigned doctor ID for the patient.
        """
        field_map = {
            'name': 'patient_name',
            'age': 'patient_age',
            'disease': 'patient_disease',
            'doctor': 'assigned_doctor_id'
        }
        if field_name in field_map:
            self.cursor.execute(
                f"""UPDATE patients SET {field_map[field_name]} = ? WHERE patient_id = ?""",
                (new_patient_data, patient_id)
            )
            self.hospital_database.commit()
        else:
            raise ValueError("Invalid field name")
    
    def delete_patient_data(self, patient_id):
        """
        Function to delete a patient's data from the database based on the patient ID.
        """
        self.cursor.execute(
            "DELETE FROM patients WHERE patient_id=?",(patient_id,)
        )
        self.hospital_database.commit()
    
    def view_patient_details(self):
        self.cursor.execute(
            "SELECT * FROM patients"
        )
        patient_details = self.cursor.fetchall()
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
        
    def get_patient_data_by_patientid(self, patient_id):
        """
        Retrieves patient data from the database based on the provided patient ID
        """
        self.cursor.execute("""
        SELECT * FROM patients WHERE patient_id = ?""",(patient_id,))
        patient_data = self.cursor.fetchone()
        if patient_data:
            return patient_data
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def get_patient_data_by_name(self, patient_name):
        """
        Retrieves patient data from the database based on the provided patient name
        """
        self.cursor.execute("""
            SELECT * FROM patients WHERE patient_name = ?""",(patient_name,)
        )
        patient_details = self.cursor.fetchall()
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()

    def get_patient_data_by_disease(self, patient_disease):
        """
        Retrieves patient data from the database based on the provided patient disease
        """
        self.cursor.execute("""
            SELECT * FROM patients WHERE patient_disease = ?""",(patient_disease,)
        )
        patient_details = self.cursor.fetchall()
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def get_patient_data_by_age_range(self, min_age, max_age):
        """
        Retrieves patient data from the database based on the provided patient age range
        """
        self.cursor.execute("""
            SELECT * FROM patients WHERE patient_age BETWEEN ? AND ?""",(min_age,max_age)
        )
        patient_details = self.cursor.fetchall()
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def get_patient_data_by_doctor(self, doctor_id):
        """
        Retrieves patient data from the database based on the provided doctor id
        """
        self.cursor.execute("""
            SELECT * FROM patients WHERE assigned_doctor_id = ?""",(doctor_id,)
        )
        patient_details = self.cursor.fetchall()
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
        
    def assign_doctor(self, patient_id, doctor_id):
        """Assigning the doctor to the patient by doctor id.
        The user inputs patient name from which patient id is retrieved"""

        #Assigning the doctor id to the patient
        self.cursor.execute("""
        UPDATE patients SET assigned_doctor_id = ? WHERE patient_id = ?""", (doctor_id ,patient_id)
        )
        self.hospital_database.commit()

    def patient_per_doctor_count(self, doctor_id):
        """
        Retrieves the number of patients based on the doctor id inputted
        """

        self.cursor.execute("""
        SELECT COUNT(*) FROM patients WHERE assigned_doctor_id = ?""", (doctor_id,)
        )
        patient_data = self.cursor.fetchone()
        if patient_data:
            return patient_data
        else:
            raise CustomExceptions.RecordNotFoundError
    
    def most_common_disease(self):
        """
        Shows the most common disease in the hospital along with how many patients are affected by it
        """
        self.cursor.execute("""
        SELECT patient_disease, COUNT(*) as count
        FROM patients 
        GROUP BY patient_disease 
        HAVING count = (SELECT MAX(count) FROM (
        SELECT COUNT(*) as count FROM patients GROUP BY patient_disease)
        )
        """)
        disease_data = self.cursor.fetchall()
        if disease_data:
            return disease_data
        else:
            raise CustomExceptions.RecordNotFoundError
    
    def most_common_age(self):
        """
        Shows the most common age in the hospital along with how many patients are of that age
        """
        self.cursor.execute("""
        SELECT patient_age, COUNT(*) as count
        FROM patients
        GROUP BY patient_age
        HAVING count = (SELECT MAX(count) FROM(
        SELECT COUNT(*) as count FROM patients GROUP BY patient_age)
        )
        """)
        age_data = self.cursor.fetchall()
        #Checking if the data actually exists
        if age_data:
            return age_data
        else:
            raise CustomExceptions.RecordNotFoundError

    def close_connection(self):
        """Close the database connection"""
        if self.hospital_database:
            self.hospital_database.close()



class DoctorTable:
    '''
    Class that handles the database operations for doctors in the Hospital Management System
    '''
    def __init__(self):
        '''
        Constructor for the DoctorDatabase class. Initializes the database connection and cursor
        '''
        self.hospital_database = sql.connect('hospital_database.db')
        self.cursor = self.hospital_database.cursor()

    def create_doctor_table(self):
        '''
        Function to create the doctors table in the database if it does not already exist
        '''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT NOT NULL,
            doctor_specialisation TEXT NOT NULL
        )''')
        self.hospital_database.commit()

    def insert_doctor(self, doctor_name, doctor_specialisation):
            """
            Function to insert a new doctor into the database
            """
            self.cursor.execute('''
                INSERT INTO doctors (doctor_name, doctor_specialisation)
                VALUES (?, ?)''', (doctor_name, doctor_specialisation)
            )
            self.hospital_database.commit()
        
    def update_doctor_data(self, doctor_id, new_doctor_data, field_name):
        """
        Function to update doctor data in the database based on the field name provided.
        *args field_name: The name of the field to be updated. It can be one of the following:
            - 'name': Updates the doctor's name.
            - 'specialisation': Updates the doctor's specialisation.
            - 'no_of_patients': Updates the number of patients assigned to the doctor.
        """
        field_map = {
            'name': 'doctor_name',
            'specialisation': 'doctor_specialisation',
        }
        if field_name in field_map:
            
            self.cursor.execute(
                f"""UPDATE doctors SET {field_map[field_name]} = ? WHERE doctor_id = ?""",
                (new_doctor_data, doctor_id)
            )
            self.hospital_database.commit()
        else:
            raise ValueError("Invalid field name")
    
    def delete_doctor_data(self, doctor_id):
        """
        Function to delete a doctor's data from the database based on the doctor ID.
        """
        self.cursor.execute(
        "DELETE FROM doctors WHERE doctor_id=?",(doctor_id,)
        )
        self.hospital_database.commit()
    
    def view_doctor_details(self):
        self.cursor.execute(
            "SELECT * FROM doctors"
        )
        doctor_details = self.cursor.fetchall()
        if doctor_details:
            return doctor_details
        else:
            raise CustomExceptions.RecordNotFoundError()

    def get_doctor_data_by_doctorid(self,doctor_id):
        """
        Retrieves doctor data from the database based on the provided doctor ID
        """
        self.cursor.execute("""
        SELECT * FROM doctors WHERE doctor_id = ?""",(doctor_id,))
        doctor_data = self.cursor.fetchone()
        if doctor_data:
            return doctor_data
        else:
            raise CustomExceptions.RecordNotFoundError()

    def get_doctor_data_by_name(self, doctor_name):
        """
        Retrieves doctor data from the database based on the provided doctor name
        """
        self.cursor.execute("""
        SELECT * FROM doctors WHERE doctor_name = ?""",(doctor_name,))
        doctor_details = self.cursor.fetchall()
        if doctor_details:
            return doctor_details
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def close_connection(self):
        """Close the database connection"""
        if self.hospital_database:
            self.hospital_database.close()