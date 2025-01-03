CREATE DATABASE healthcare_system;

-- Menggunakan database healthcare_system
    \c healthcare_system;

-- Tabel untuk pasien
CREATE TABLE patients (patient_id SERIAL PRIMARY KEY,name VARCHAR(100) NOT NULL,age INTEGER NOT NULL,gender VARCHAR(10));

-- Tabel untuk dokter
CREATE TABLE  doctors (doctor_id SERIAL PRIMARY KEY,name VARCHAR(100) NOT NULL,specialization VARCHAR(100));

-- Tabel untuk catatan medis
CREATE TABLE  medical_records (record_id SERIAL PRIMARY KEY,patient_id INTEGER REFERENCES patients(patient_id) ON DELETE CASCADE,doctor_id INTEGER REFERENCES doctors(doctor_id) ON DELETE CASCADE,diagnosis TEXT,treatment TEXT,date DATE);

\dt




DROP DATABASE nama_database;

INSERT INTO patients (name, age, gender) VALUES('Budi', 30, 'Male'),('Cahyani', 25, 'Female'),('Putri', 40, 'Female');

INSERT INTO doctors (name, specialization) VALUES('Dr. Mike Brown', 'Cardiology'),('Dr. Sarah Connor', 'Jantung'),('Dr. Emily Davis', 'Paru-Paru');

INSERT INTO medical_records (patient_id, doctor_id, diagnosis, treatment, date) VALUES(1, 1, 'Hipertensi', 'Meditasi', '2024-01-15'),(2, 2, 'Jantung Berdebar Cepat', 'Istirahat', '2024-02-10'),(3, 3, 'Sesak', 'Berhenti Merokok', '2024-03-05');