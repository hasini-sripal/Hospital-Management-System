import unittest as Test
from HospitalDatabase import PatientTable, DoctorTable
import os
import CustomExceptions
from datetime import datetime
    

class TestHospitalManagement(Test.TestCase):
    
    def setUp(self) -> None:
        """Creating a new database from scratch for each test case"""
        
        test_name = self._testMethodName
        self.test_db = f"{test_name}.db"
        
        self.patient_db = PatientTable()
        self.doctor_db = DoctorTable()
        
        self.patient_db.db_name = self.doctor_db.db_name = self.test_db
        self.patient_db.create_patient_table()
        self.doctor_db.create_doctor_table()
    
    def tearDown(self) -> None:
        import time
        import gc 

        gc.collect()
        
        time.sleep(0.3)
        
        for i in range(5):
            try:
                if os.path.exists(self.test_db):
                    os.remove(self.test_db)
                    break
            except:
                time.sleep(0.2)

    #######___ POSITIVE TEST CASES ___#######


    # ==================== test 1 ====================
    def test_insert_patient(self) ->None:
        """Testing if patient details can be inserted"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu",created_at)

        patients = self.patient_db.view_patient_details()
        patient_data = patients[0]

        #Checking if only one patient is added
        self.assertEqual(len(patients),1)
        #Checking if the patient name is equal to Laila
        self.assertEqual(patient_data[2], "Laila")
        #Checking if the patient age is equal to 25
        self.assertEqual(patient_data[3],25)
        #Checking if the patient disease is equal to Flu
        self.assertEqual(patient_data[4],'Flu')
        #Checking if the time of admission is equal to created_at
        self.assertEqual(patient_data[5],created_at)
        

    # ==================== test 2 ====================
    def test_insert_doctor(self) ->None:
        """Testing if doctor details can be inserted"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.doctor_db.insert_doctor('Laila','Neurology',created_at)

        doctors = self.doctor_db.view_doctor_details()
        doctor_data = doctors[0]

        #Checking if only one doctor is added
        self.assertEqual(len(doctors),1)
        #Checking if the doctor name is equal to Laila
        self.assertEqual(doctor_data[1],'Laila')
        #Checking if the doctor specialisation is equal to Neurology
        self.assertEqual(doctor_data[2],'Neurology')
        #Checking if the time of joining of doctor matches created_at
        self.assertEqual(doctor_data[3],created_at)

    # ==================== test 3 ====================
    def test_get_patient_by_id(self) ->None:
        """Testing if the patient details can be obtained by patient id"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu",created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        patient_data = self.patient_db.get_patient_data_by_patientid(patient_id)

        #Checking if the patient name is equal to Laila
        self.assertEqual(patient_data[2], "Laila")
        #Checking if the patient age is equal to 25
        self.assertEqual(patient_data[3],25)
        #Checking if the patient disease is equal to Flu
        self.assertEqual(patient_data[4],'Flu')
        #Checking if the time of admission of patient matches created_at
        self.assertEqual(patient_data[5],created_at)

    # ==================== test 4 ====================
    def test_get_doctor_by_id(self) ->None:
        """Testing if the doctor details can be obtained by doctor id"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.doctor_db.insert_doctor('Laila','Neurology',created_at)

        doctor_id = self.doctor_db.get_last_inserted_doctor_id()
        doctor_data = self.doctor_db.get_doctor_data_by_doctorid(doctor_id)

        #Checking if the doctor name is equal to Laila
        self.assertEqual(doctor_data[1],'Laila')
        #Checking if the doctor specialisation is equal to Neurology
        self.assertEqual(doctor_data[2],'Neurology')
        #Checking if the time of joining of doctor matches created_at
        self.assertEqual(doctor_data[3],created_at)
    
    # ==================== test 5 ====================
    def test_get_patient_by_name(self) ->None:
        """Testing if the patient details can be obtained by patient id"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu",created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        patient_data = self.patient_db.get_patient_data_by_name('Laila')

        #Checking if the patient id is equal to last inserted patient id
        self.assertEqual(patient_data[0][0], patient_id)
        #Checking if the patient age is equal to 25
        self.assertEqual(patient_data[0][3],25)
        #Checking if the patient disease is equal to Flu
        self.assertEqual(patient_data[0][4],'Flu')
        #Checking if the time of admission of patient matches created_at
        self.assertEqual(patient_data[0][5],created_at)

    # ==================== test 6 ====================
    def test_delete_patient(self) ->None:
        """Testing if patient details can be deleted"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu", created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        self.patient_db.delete_patient_data(patient_id)

        #Checking if the RecordNotFoundError exception is raised when no data exists in the database
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_patientid(patient_id)

    # ==================== test 7 ====================
    def test_delete_doctor(self) ->None:
        """Testing if doctor details can be deleted"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.doctor_db.insert_doctor("Laila","Neurology", created_at)

        doctor_id = self.doctor_db.get_last_inserted_doctor_id()
        self.doctor_db.delete_doctor_data(doctor_id)

        #Checking if the RecordNotFoundError exception is raised when no data exists in the database
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.doctor_db.get_doctor_data_by_doctorid(doctor_id)

    # ==================== test 8 ====================
    def test_update_patient_name(self) ->None:
        """Testing if patient name can be updated"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu",created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        self.patient_db.update_patient_details(patient_id, "Lola", 'name')

        patient = self.patient_db.get_patient_data_by_patientid(patient_id)

        #Checking if the name of the patient has changed to Lola
        self.assertEqual(patient[2],'Lola')

    # ==================== test 9 ====================
    def test_update_doctor_specialisation(self) ->None:
        """Testing if the doctor specialisation can be updated"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.doctor_db.insert_doctor("Laila","Neurology",created_at)

        doctor_id = self.doctor_db.get_last_inserted_doctor_id()
        self.doctor_db.update_doctor_data(doctor_id, 'Cardiology', 'specialisation')

        doctor = self.doctor_db.get_doctor_data_by_doctorid(doctor_id)

        #Checkinf if the specialisaion has changed to Cardiology
        self.assertEqual(doctor[2],'Cardiology')

    # ==================== test 10 ====================
    def test_created_at(self) ->None:
        """Testing if the timestamp is saved on insert"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila", 25, "Fever",created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        patient = self.patient_db.get_patient_data_by_patientid(patient_id)

        #Checking if timestamp is saved on insert
        self.assertIsNotNone(patient[5])

    # ==================== test 11 ====================
    def test_config_loader(self) ->None:
        """Testing if config_loader.json is loaded correctly and fallback works when file is missing"""

        import config_loader
        config = config_loader.load_config('config.json')

        #Checking if config has a tangible value
        self.assertIsNotNone(config)

        #Checking if config has database key
        self.assertIn("database", config)

    # ==================== test 12 =====================
    def test_multiple_patients_insert(self) ->None:
        """Testing if multiple patients can be inserted"""
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.patient_db.insert_patient("John", 25, "Flu", created_at)
        self.patient_db.insert_patient("Jane", 30, "Cold", created_at)
        self.patient_db.insert_patient("Bob", 40, "Fever", created_at)

        patients = self.patient_db.view_patient_details()

        #Checking if 3 patient details are entered
        self.assertEqual(len(patients), 3)

    # ==================== test 13 =====================
    def test_update_patient_age(self) ->None:
        """Testing if patient age can be updated"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila", 25, "Flu", created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        self.patient_db.update_patient_details(patient_id, 30, 'age')

        patient = self.patient_db.get_patient_data_by_patientid(patient_id)

        #Checking if patient age has changed to 30
        self.assertEqual(patient[3], 30)

    # ==================== test 14 =====================
    def test_update_patient_disease(self) ->None:
        """Testing if patient disease can be updated"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila", 25, "Flu", created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()        
        self.patient_db.update_patient_details(patient_id, 'Dengue', 'disease')

        patient = self.patient_db.get_patient_data_by_patientid(patient_id)
        
        self.assertEqual(patient[4], 'Dengue')

    # ==================== test 15 =====================
    def test_update_assigned_doctor(self) ->None:
        """Testing if assigned doctor can be updated"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila", 25, "Flu", created_at)
        self.doctor_db.insert_doctor("Laila",'General Physician',created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        doctor_id = self.doctor_db.get_last_inserted_doctor_id()

        self.patient_db.update_patient_details(patient_id, doctor_id, 'doctor')

        patient = self.patient_db.get_patient_data_by_patientid(patient_id)
        
        self.assertEqual(patient[1], doctor_id)

    # ==================== test 16 ====================
    def test_get_patient_by_disease(self) ->None:
        """Testing if patient details can be obtained by disease"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu",created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        patient_data = self.patient_db.get_patient_data_by_disease('Flu')

        #Checking if the patient name is equal to Laila
        self.assertEqual(patient_data[0][2], "Laila")
        #Checking if the patient age is equal to 25
        self.assertEqual(patient_data[0][3],25)
        #Checking if the patient id is equal to last inserted patient id
        self.assertEqual(patient_data[0][0], patient_id)
        #Checking if the time of admission of patient matches created_at
        self.assertEqual(patient_data[0][5],created_at)

    # ==================== test 17 =====================
    def test_get_patient_by_age_range(self) ->None:
        """Testing if patient details can be obtained by age range"""
    
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila",25,"Flu",created_at)

        patient_data_1 = self.patient_db.get_patient_data_by_age_range(2,60) #Normal
        patient_data_2 = self.patient_db.get_patient_data_by_age_range(24,25) #Edge Case 1
        patient_data_3 = self.patient_db.get_patient_data_by_age_range(25,26) #Edge Case 2

        #Checking if patient name is equal to Laila for Normal Case
        self.assertEqual(patient_data_1[0][2], 'Laila')

        #Checking if patient name is equal to Laila for Edge Cases
        self.assertEqual(patient_data_2[0][2], 'Laila')
        self.assertEqual(patient_data_3[0][2], 'Laila')

    # ==================== test 18 =====================
    def test_get_patient_by_assigned_doctor(self) ->None:
        """Testing if patient detials can be obtained by assigned doctor"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila", 25, "Flu", created_at)
        self.doctor_db.insert_doctor("Laila",'General Physician',created_at)

        
        patient_id = self.patient_db.get_last_inserted_patient_id()
        doctor_id = self.doctor_db.get_last_inserted_doctor_id()
        
        #Assigning the doctor to the patient
        self.patient_db.assign_doctor(patient_id, doctor_id)

        patient_data = self.patient_db.get_patient_data_by_doctor(doctor_id)

        #Checking if the patient name is equal to Laila
        self.assertEqual(patient_data[0][2], "Laila")
        #Checking if the patient age is equal to 25
        self.assertEqual(patient_data[0][3], 25)
        #Checking if the patient disease is equal to Flu
        self.assertEqual(patient_data[0][4], 'Flu')
        #Checking if the time of admission of patient matches created_at
        self.assertEqual(patient_data[0][5], created_at)
        #Chcking if the patient_id is equal to last inserted patient id
        self.assertEqual(patient_data[0][0], patient_id)

    # ==================== test 19 =====================
    def test_assign_doctor(self) ->None:
        """Testing if doctor can be assigned"""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_db.insert_patient("Laila", 25, "Flu", created_at)
        self.doctor_db.insert_doctor("Laila",'General Physician',created_at)

        patient_id = self.patient_db.get_last_inserted_patient_id()
        doctor_id = self.doctor_db.get_last_inserted_doctor_id()

        self.patient_db.assign_doctor(patient_id, doctor_id)

        patient = self.patient_db.get_patient_data_by_patientid(patient_id)
        
        self.assertEqual(patient[1], doctor_id)

    # ==================== test 20 =====================
    def test_get_doctor_by_name(self) ->None:
        """Testing if doctor details can be obtained by name"""
 
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.doctor_db.insert_doctor('Laila','Neurology',created_at)

        doctor_id = self.doctor_db.get_last_inserted_doctor_id()
        doctor_data = self.doctor_db.get_doctor_data_by_name('Laila')
 
        #Checking if the doctor name is equal to Laila
        self.assertEqual(doctor_data[0][1],'Laila')
        #Checking if the doctor id is equal to last inserted doctor id
        self.assertEqual(doctor_data[0][0], doctor_id)
        #Checking if the time of joining of doctor matches created_at
        self.assertEqual(doctor_data[0][3],created_at)


    #######___ NEGATIVE TEST CASES ___######

    # ==================== test 21 =====================
    def test_record_not_found_for_id(self) ->None:
        """Testing if RecordNotFoundError exception is raised when searching for a non-existing ID"""

        #Raises when patient id doesn't exists
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_patientid(9999)

        #Raises when assigned doctor id does not exist
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_doctor(999)

        #Raises when doctor id does not exist in the database
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.doctor_db.get_doctor_data_by_doctorid(9999)

    # ==================== test 22 =====================
    def test_record_not_found_non_existent_records(self) ->None:
        """Testing if RecordNotFoundError exception is raised when records are not available"""

        #Raises when patient records do not exist in database
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.view_patient_details()

        #Raises when doctor records do not exist in database
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.doctor_db.view_doctor_details()

    # ==================== test 23 =====================
    def test_record_not_found_for_name(self) ->None:
        """Testing if RecordNotFoundError exception is raised when name does not exist"""

        #Raises when patient name does not exist
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_name('Laila')

        #Raises when doctor name does not exist
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.doctor_db.get_doctor_data_by_name('Laila')

    # ==================== test 24 =====================
    def test_record_not_found_for_disease(self) ->None:
        """Testing if RecordNotFoundError exception is raised when the disease does not exist"""

        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_disease('Flu')
    
    # ==================== test 25 =====================
    def test_record_not_found_for_age_range(self) ->None:
        """Testing if RecordNotFoundError exception is raised when the age range does not exist"""

        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_age_range(1,30)

    # ==================== test 26 ======================
    def test_record_not_found_for_doctor(self) ->None:
        """Testing if RecordNotFoundError exception is raised when the assigned doctor does not exist"""

        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.get_patient_data_by_doctor(9999)

    # ==================== test 27 ======================
    def test_record_not_found_for_simple_report(self) ->None:
        """Testing if RecordNotFoundError exception is raised when the records for simple report does not exist"""

        #Raises when disease count cannot be shown due to non-existent records
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.disease_count()

        #Raises when no records exist to show most common disease
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.most_common_disease()

        #Raises when no records exist to show most common age
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.most_common_age()

        #Raises when the doctor id does not exist for the does not exist for the patient per doctor count to be shown
        with self.assertRaises(CustomExceptions.RecordNotFoundError):
            self.patient_db.patient_per_doctor_count(99999)

        
if __name__ == '__main__':
    Test.main()