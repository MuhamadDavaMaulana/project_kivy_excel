import pandas as pd
import psycopg2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

Window.size = (700, 600)

def connect_db():
    try:
        return psycopg2.connect(
            dbname="healthcare_system",
            user="postgres",
            password="admin04",
            host="localhost"
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# CRUD pasien
def add_patient(name, age, gender):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)", (name, age, gender))
            engine.commit()

def update_patient(patient_id, name, age,gender):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("UPDATE patients SET name=%s, age=%s, gender=%s WHERE patient_id=%s", (name, age, gender, patient_id))
            engine.commit()

def delete_patient(patient_id):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("DELETE FROM patients WHERE patient_id=%s", (patient_id,))
            engine.commit()

def get_patients():
    engine = connect_db()
    if engine:
        query = "SELECT * FROM patients"
        df = pd.read_sql(query, engine)
        return df
    return pd.DataFrame()

# CRUD dokter
def add_doctor(name, specialization):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("INSERT INTO doctors (name, specialization) VALUES (%s, %s)", (name, specialization))
            engine.commit()

def update_doctor(doctor_id, name, specialization):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("UPDATE doctors SET name=%s, specialization=%s WHERE doctor_id=%s", (name, specialization, doctor_id))
            engine.commit()

def delete_doctor(doctor_id):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("DELETE FROM doctors WHERE doctor_id=%s", (doctor_id,))
            engine.commit()

def get_doctors():
    engine = connect_db()
    if engine:
        query = "SELECT * FROM doctors"
        df = pd.read_sql(query, engine)
        return df
    return pd.DataFrame()

# CRUD medical records
def add_medical_record(patient_id, doctor_id, diagnosis, treatment, date):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("INSERT INTO medical_records (patient_id, doctor_id, diagnosis, treatment, date) VALUES (%s, %s, %s, %s, %s)", (patient_id, doctor_id, diagnosis, treatment, date))
            engine.commit()

def get_medical_records():
    engine = connect_db()
    if engine:
        query = "SELECT * FROM medical_records"
        df = pd.read_sql(query, engine)
        return df
    return pd.DataFrame()

def update_medical_record(record_id, patient_id, doctor_id, diagnosis, treatment, date):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("UPDATE medical_records SET patient_id=%s, doctor_id=%s, diagnosis=%s, treatment=%s, date=%s WHERE record_id=%s", (patient_id, doctor_id, diagnosis, treatment, date, record_id))
            engine.commit()

def delete_medical_record(record_id):
    engine = connect_db()
    if engine:
        with engine.cursor() as conn:
            conn.execute("DELETE FROM medical_records WHERE record_id=%s", (record_id,))
            engine.commit()

def export_medical_records_to_excel():
    engine = connect_db()
    query = "SELECT * FROM medical_records;"
    df = pd.read_sql_query(query, engine)
    df.to_excel("medical_records.xlsx", index=False, sheet_name="medical_record")
    print("Laporan berhasil disimpan")

class PatientApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)


        self.patient_dropdown = DropDown()
        self.patient_select_button = Button(text='Select Patient', background_color=(1, 1, 0, 1))  
        self.patient_select_button.bind(on_release=self.patient_dropdown.open)
        layout.add_widget(self.patient_select_button)

        self.patient_dropdown.bind(on_select=self.display_patient)
        self.populate_patient_dropdown()

        # Input pasien
        self.patient_input = TextInput(hint_text='Enter Patient Name', multiline=False)
        layout.add_widget(self.patient_input)

        self.age_input = TextInput(hint_text='Enter Patient Age', multiline=False)
        layout.add_widget(self.age_input)

        self.gender_input = TextInput(hint_text='Enter Patient Gender', multiline=False)
        layout.add_widget(self.gender_input)

        self.patient_id_input = TextInput(hint_text='Enter Patient ID (for delete)', multiline=False)
        layout.add_widget(self.patient_id_input)

        add_patient_button = Button(text='Add Patient', background_color=(0, 1, 0, 1)) 
        add_patient_button.bind(on_press=self.add_patient)
        layout.add_widget(add_patient_button)

        update_patient_button = Button(text='Update Patient', background_color=(0.5, 0.5, 0.5, 1))  
        update_patient_button.bind(on_press=self.update_patient)
        layout.add_widget(update_patient_button)

        delete_patient_button = Button(text='Delete Patient', background_color=(1, 0, 0, 1))  
        delete_patient_button.bind(on_press=self.delete_patient)
        layout.add_widget(delete_patient_button)

        # Dropdown dokter
        self.doctor_dropdown = DropDown()
        self.doctor_select_button = Button(text='Select Doctor', background_color=(1, 1, 0, 1))  
        self.doctor_select_button.bind(on_release=self.doctor_dropdown.open)
        layout.add_widget(self.doctor_select_button)

        self.doctor_dropdown.bind(on_select=self.display_doctor)
        self.populate_doctor_dropdown()

        # Input  dokter
        self.doctor_input = TextInput(hint_text='Enter Doctor Name', multiline=False)
        layout.add_widget(self.doctor_input)

        self.specialization_input = TextInput(hint_text='Enter Doctor Specialization', multiline=False)
        layout.add_widget(self.specialization_input)

        self.doctor_id_input = TextInput(hint_text='Enter Doctor ID (for update/delete)', multiline=False)
        layout.add_widget(self.doctor_id_input)

        add_doctor_button = Button(text='Add Doctor', background_color=(0, 1, 0, 1)) 
        add_doctor_button.bind(on_press=self.add_doctor)
        layout.add_widget(add_doctor_button)

        update_doctor_button = Button(text='Update Doctor', background_color=(0.5, 0.5, 0.5, 1))  
        update_doctor_button.bind(on_press=self.update_doctor)
        layout.add_widget(update_doctor_button)

        delete_doctor_button = Button(text='Delete Doctor', background_color=(1, 0, 0, 1))  
        delete_doctor_button.bind(on_press=self.delete_doctor)
        layout.add_widget(delete_doctor_button)

        # Dropdown medical records
        self.record_dropdown = DropDown()
        self.record_select_button = Button(text='Select Medical Record', background_color=(1, 1, 0, 1))  
        self.record_select_button.bind(on_release=self.record_dropdown.open)
        layout.add_widget(self.record_select_button)

        self.record_dropdown.bind(on_select=self.display_medical_record)
        self.populate_record_dropdown()

        # Input  medical records
        self.record_input = TextInput(hint_text='Enter Diagnosis', multiline=False)
        layout.add_widget(self.record_input)

        self.treatment_input = TextInput(hint_text='Enter Treatment', multiline=False)
        layout.add_widget(self.treatment_input)

        self.date_input = TextInput(hint_text='Enter Date (YYYY-MM-DD)', multiline=False)
        layout.add_widget(self.date_input)

        self.selected_patient_id_input = TextInput(hint_text='Enter Patient ID for Medical Record', multiline=False)
        layout.add_widget(self.selected_patient_id_input)

        self.selected_doctor_id_input = TextInput(hint_text='Enter Doctor ID for Medical Record', multiline=False)
        layout.add_widget(self.selected_doctor_id_input)

        self.record_id_input = TextInput(hint_text='Enter Record ID (for update/delete)', multiline=False)
        layout.add_widget(self.record_id_input)

        add_record_button = Button(text='Add Medical Record', background_color=(0, 1, 0, 1)) 
        add_record_button.bind(on_press=self.add_medical_record)
        layout.add_widget(add_record_button)


        export_button = Button(text='Export Medical Records to Excel', background_color=(0, 0, 1, 1))  # Biru
        export_button.bind(on_press=lambda instance: export_medical_records_to_excel())
        layout.add_widget(export_button)

        return layout

    def populate_patient_dropdown(self):
        self.patient_dropdown.clear_widgets()
        patients = get_patients()
        for index, row in patients.iterrows():
            btn = Button(text=row['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.patient_dropdown.select(btn.text))
            self.patient_dropdown.add_widget(btn)

    def display_patient(self, instance, name):
        patients = get_patients()
        patient_info = patients[patients['name'] == name].iloc[0]
        self.patient_id_input.text = str(patient_info['patient_id'])
        self.patient_input.text = patient_info['name']
        self.age_input.text = str(patient_info['age'])
        self.gender_input.text = patient_info['gender']

    def add_patient(self, instance):
        name = self.patient_input.text
        age = self.age_input.text
        gender = self.gender_input.text
        add_patient(name, age, gender)
        self.populate_patient_dropdown()

    def update_patient(self, instance):
        patient_id = self.patient_id_input.text
        name = self.doctor_input.text
        age = self.age_input.text
        gender = self.gender_input.text
        update_patient(patient_id, name, age,gender)
        self.populate_doctor_dropdown()

    def delete_patient(self, instance):
        patient_id = self.patient_id_input.text
        delete_patient(patient_id)
        self.populate_patient_dropdown()

    def populate_doctor_dropdown(self):
        self.doctor_dropdown.clear_widgets()
        doctors = get_doctors()
        for index, row in doctors.iterrows():
            btn = Button(text=f'Doctor Name: {row["name"]} - Specialization: {row["specialization"]}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.doctor_dropdown.select(btn.text))
            self.doctor_dropdown.add_widget(btn)

    def display_doctor(self, instance, name):
        doctors = get_doctors()
        doctor_info = doctors[doctors['name'] == name].iloc[0]
        self.doctor_id_input.text = str(doctor_info['doctor_id'])
        self.doctor_input.text = doctor_info['name']
        self.specialization_input.text = doctor_info['specialization']

    def add_doctor(self, instance):
        name = self.doctor_input.text
        specialization = self.specialization_input.text
        add_doctor(name, specialization)
        self.populate_doctor_dropdown()

    def update_doctor(self, instance):
        doctor_id = self.doctor_id_input.text
        name = self.doctor_input.text
        specialization = self.specialization_input.text
        update_doctor(doctor_id, name, specialization)
        self.populate_doctor_dropdown()

    def delete_doctor(self, instance):
        doctor_id = self.doctor_id_input.text
        delete_doctor(doctor_id)
        self.populate_doctor_dropdown()

    def populate_record_dropdown(self):
        self.record_dropdown.clear_widgets()
        records = get_medical_records()
        for index, row in records.iterrows():
            btn = Button(text=f'Record ID: {row["record_id"]} - Pasien ID: {row["patient_id"]} - Dokter ID: {row["doctor_id"]} - Diagnosis: {row["diagnosis"]}- Treatment: {row["treatment"]}- Date: {row["date"]}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.record_dropdown.select(btn.text))
            self.record_dropdown.add_widget(btn)

    def display_medical_record(self, instance, text):
        record_id = text.split(" - ")[0].split(": ")[1]
        records = get_medical_records()
        record_info = records[records['record_id'] == int(record_id)].iloc[0]
        self.record_id_input.text = str(record_info['record_id'])
        self.doctor_id_input.text = str(record_info['doctor_id'])
        self.record_input.text = record_info['diagnosis']
        self.treatment_input.text = record_info['treatment']
        self.date_input.text = str(record_info['date'])
    def add_medical_record(self, instance):
        patient_id = self.patient_id_input.text  # ID pasien dari input
        doctor_id = self.selected_doctor_id_input.text  # ID dokter
        diagnosis = self.record_input.text  # Diagnosis
        treatment = self.treatment_input.text  
        date = self.date_input.text 
        add_medical_record(patient_id, doctor_id, diagnosis, treatment, date)
        self.populate_record_dropdown()

if __name__ == '__main__':
    PatientApp().run()