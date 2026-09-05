"""

Controls the Database Management of the Hospital Management System.
Contains:
1. PatientDatabase class
2. DoctorDatabase class

"""
import sqlite3 as sql
import CustomExceptions, config_loader

class PatientTable:
    '''
    Class that handles the database operations for patients in the Hospital Management System
    '''
    def __init__(self) -> None:
        '''
        Constructor for the PatientDatabase class. Initializes the database connection and cursor
        '''
        config = config_loader.load_config('config.json')
        self.db_name = config.get("database", "hospital_database.db")

    def get_last_inserted_patient_id(self) -> int:
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("SELECT MAX(patient_id) FROM patients")
            result = cursor.fetchone()
            if result and result[0]:
                return result[0]
            else:
                raise CustomExceptions.RecordNotFoundError()
    
    def create_patient_table(self) -> None:
        '''
        Function to create the patients table in the database if it does not already exist
        '''
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                assigned_doctor_id INTEGER REFERENCES doctors(doctor_id),
                patient_name TEXT NOT NULL,
                patient_age INTEGER NOT NULL,
                patient_disease TEXT NOT NULL,
                created_at TEXT)'''
            )
            

    def insert_patient(self, patient_name:str, patient_age:int, patient_disease:str, created_at:str) -> None:
        '''
        Function to insert a new patient into the database
        '''
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute('''
                INSERT INTO patients (patient_name, patient_age, patient_disease, created_at)
                VALUES (?, ?, ?, ?)''', (patient_name, patient_age, patient_disease, created_at)
            )
            hospital_database.commit()
            
        
    def update_patient_details(self, patient_id:int, new_patient_data, field_name:str) -> None:
        """
        Function to update patient data in the database based on the field name provided
        *args field_name: The name of the field to be updated. It can be one of the following:
            - 'name': Updates the patient's name. 
            - 'age': Updates the patient's age.
            - 'disease': Updates the patient's disease.
            - 'doctor': Updates the assigned doctor ID for the patient.
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            field_map = {
                'name': 'patient_name',
                'age': 'patient_age',
                'disease': 'patient_disease',
                'doctor': 'assigned_doctor_id'
            }
            if field_name in field_map:
                cursor.execute(
                    f"""UPDATE patients SET {field_map[field_name]} = ? WHERE patient_id = ?""",
                    (new_patient_data, patient_id)
                )
                hospital_database.commit()
                
            else:
                raise ValueError("Invalid field name")
    
    def delete_patient_data(self, patient_id:int) -> None:
        """
        Function to delete a patient's data from the database based on the patient ID.
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute(
                "DELETE FROM patients WHERE patient_id=?",(patient_id,)
            )
            hospital_database.commit()

    def view_patient_details(self) -> list:
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute(
                "SELECT * FROM patients"
            )
            patient_details = cursor.fetchall()
            
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
        
    def get_patient_data_by_patientid(self, patient_id:int) -> tuple:
        """
        Retrieves patient data from the database based on the provided patient ID
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
        SELECT * FROM patients WHERE patient_id = ?""",(patient_id,))
            patient_data = cursor.fetchone()

        if patient_data:
            return patient_data
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def get_patient_data_by_name(self, patient_name:str) -> list:
        """
        Retrieves patient data from the database based on the provided patient name
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
                SELECT * FROM patients WHERE patient_name = ?""",(patient_name,)
            )
            patient_details = cursor.fetchall()
  
        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()

    def get_patient_data_by_disease(self, patient_disease:str) -> list:
        """
        Retrieves patient data from the database based on the provided patient disease
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
                SELECT * FROM patients WHERE patient_disease = ?""",(patient_disease,)
            )
            patient_details = cursor.fetchall()


        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def get_patient_data_by_age_range(self, min_age:int, max_age:int) -> list:
        """
        Retrieves patient data from the database based on the provided patient age range
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
                SELECT * FROM patients WHERE patient_age BETWEEN ? AND ?""",(min_age,max_age)
            )
            patient_details = cursor.fetchall()

        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def get_patient_data_by_doctor(self, doctor_id:int) -> list:
        """
        Retrieves patient data from the database based on the provided doctor id
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
                SELECT * FROM patients WHERE assigned_doctor_id = ?""",(doctor_id,)
            )
            patient_details = cursor.fetchall()

        if patient_details:
            return patient_details
        else:
            raise CustomExceptions.RecordNotFoundError()            
        
    def assign_doctor(self, patient_id:int, doctor_id:int) -> None:
        """Assigning the doctor to the patient by doctor id.
        The user inputs patient name from which patient id is retrieved"""

        #Assigning the doctor id to the patient
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
            UPDATE patients SET assigned_doctor_id = ? WHERE patient_id = ?""", (doctor_id ,patient_id)
            )
            hospital_database.commit()

    def disease_count(self) -> tuple:
        """
        Retrieves the Disease Name and the Disease count
        """

        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute(
                "SELECT patient_disease, COUNT(*) FROM patients GROUP BY patient_disease ORDER BY COUNT(*) DESC"
            )
            patient_data = cursor.fetchall()

        if patient_data:
            return patient_data
        else:
            raise CustomExceptions.RecordNotFoundError()

    def patient_per_doctor_count(self, doctor_id:int) -> int:
        """
        Retrieves the number of patients based on the doctor id inputted
        """

        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
            SELECT COUNT(*) FROM patients WHERE assigned_doctor_id = ?""", (doctor_id,)
            )  
            patient_data = cursor.fetchone()

        if patient_data and patient_data[0]:
            return patient_data
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def most_common_disease(self) -> list:
        """
        Shows the most common disease in the hospital along with how many patients are affected by it
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
        SELECT patient_disease, COUNT(*) as count
        FROM patients 
        GROUP BY patient_disease 
        HAVING count = (SELECT MAX(count) FROM (
        SELECT COUNT(*) as count FROM patients GROUP BY patient_disease)
        )
        """)
        disease_data = cursor.fetchall()
  
        if disease_data:
            return disease_data
        else:
            raise CustomExceptions.RecordNotFoundError()
    
    def most_common_age(self) -> list:
        """
        Shows the most common age in the hospital along with how many patients are of that age
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
        SELECT patient_age, COUNT(*) as count
        FROM patients
        GROUP BY patient_age
        HAVING count = (SELECT MAX(count) FROM(
        SELECT COUNT(*) as count FROM patients GROUP BY patient_age)
        )
        """)
        age_data = cursor.fetchall()

        #Checking if the data actually exists
        if age_data:
            return age_data
        else:
            raise CustomExceptions.RecordNotFoundError()



class DoctorTable:
    '''
    Class that handles the database operations for doctors in the Hospital Management System
    '''
    def __init__(self) -> None:
        '''
        Constructor for the DoctorDatabase class. Initializes the database connection and cursor
        '''
        config = config_loader.load_config('config.json')
        self.db_name = config.get("database", "hospital_database.db")

    def get_last_inserted_doctor_id(self) -> int:
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("SELECT MAX(doctor_id) FROM doctors")
            result = cursor.fetchone()
            if result and result[0]:
                return result[0]
            else:
                raise CustomExceptions.RecordNotFoundError()
    
    
    def create_doctor_table(self) -> None:
        '''
        Function to create the doctors table in the database if it does not already exist
        '''
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_name TEXT NOT NULL,
                doctor_specialisation TEXT NOT NULL,
                created_at TEXT
            )''')
            hospital_database.commit()

    def insert_doctor(self, doctor_name:str, doctor_specialisation:str, created_at:str) -> None:
            """
            Function to insert a new doctor into the database
            """
            with sql.connect(self.db_name) as hospital_database:
                cursor = hospital_database.cursor()
                cursor.execute('''
                    INSERT INTO doctors (doctor_name, doctor_specialisation, created_at)
                    VALUES (?, ?, ?)''', (doctor_name, doctor_specialisation, created_at)
                )
                hospital_database.commit()
                
                
        
    def update_doctor_data(self, doctor_id:int, new_doctor_data, field_name:str) -> None:
        """
        Function to update doctor data in the database based on the field name provided.
        *args field_name: The name of the field to be updated. It can be one of the following:
            - 'name': Updates the doctor's name.
            - 'specialisation': Updates the doctor's specialisation
        """
        field_map = {
            'name': 'doctor_name',
            'specialisation': 'doctor_specialisation',
        }
        if field_name in field_map:
            with sql.connect(self.db_name) as hospital_database:
                cursor = hospital_database.cursor()
                cursor.execute(
                    f"""UPDATE doctors SET {field_map[field_name]} = ? WHERE doctor_id = ?""",
                    (new_doctor_data, doctor_id)
                )
                hospital_database.commit()
                
        else:
            raise ValueError("Invalid field name")
         
    def delete_doctor_data(self, doctor_id:int) -> None:
        """
        Function to delete a doctor's data from the database based on the doctor ID.
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute(
                "DELETE FROM doctors WHERE doctor_id=?", (doctor_id,)
            )
            hospital_database.commit()
            
            
    def view_doctor_details(self) -> list:
        """
        Function to view all doctor details from the database
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute(
                "SELECT * FROM doctors"
            )
            doctor_details = cursor.fetchall()
            
        if doctor_details:
            return doctor_details
        else:
            raise CustomExceptions.RecordNotFoundError()

    def get_doctor_data_by_doctorid(self,doctor_id:int) -> tuple:
        """
        Retrieves doctor data from the database based on the provided doctor ID
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
            SELECT * FROM doctors WHERE doctor_id = ?""",(doctor_id,))
            doctor_data = cursor.fetchone()
            
        if doctor_data:
            return doctor_data
        else:
            raise CustomExceptions.RecordNotFoundError()

    def get_doctor_data_by_name(self, doctor_name:str) -> list:
        """
        Retrieves doctor data from the database based on the provided doctor name
        """
        with sql.connect(self.db_name) as hospital_database:
            cursor = hospital_database.cursor()
            cursor.execute("""
            SELECT * FROM doctors WHERE doctor_name = ?""",(doctor_name,))
            doctor_details = cursor.fetchall()
            
        if doctor_details:
            return doctor_details
        else:
            raise CustomExceptions.RecordNotFoundError()
