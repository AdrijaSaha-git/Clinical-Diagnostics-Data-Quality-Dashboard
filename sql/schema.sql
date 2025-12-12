CREATE DATABASE IF NOT EXISTS clinical_lab;
USE clinical_lab;

-- Basic patient info
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_code VARCHAR(20) NOT NULL,
    sex ENUM('M','F','O') NULL,
    dob DATE NULL
);

-- Sample metadata
CREATE TABLE samples (
    sample_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    sample_date DATETIME NOT NULL,
    sample_type VARCHAR(20),         -- e.g., Serum
    analyzer_id VARCHAR(20),         -- Analyzer_A / Analyzer_B
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- Test results (lab analytes)
CREATE TABLE test_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    sample_id INT NOT NULL,
    analyte_name VARCHAR(50) NOT NULL,        -- GLUCOSE, UREA, etc.
    result_value DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20),
    reference_low DECIMAL(10,2),
    reference_high DECIMAL(10,2),
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);

-- QC logs (control runs)
CREATE TABLE qc_logs (
    qc_id INT AUTO_INCREMENT PRIMARY KEY,
    run_datetime DATETIME NOT NULL,
    analyte_name VARCHAR(50) NOT NULL,
    level VARCHAR(20),                        -- Level 1, Level 2
    qc_value DECIMAL(10,2) NOT NULL,
    target_value DECIMAL(10,2) NOT NULL,
    sd DECIMAL(10,2) NOT NULL,               -- standard deviation
    status ENUM('PASS','FAIL') NOT NULL
);

-- Calibration logs (for drift)
CREATE TABLE calibration_logs (
    calib_id INT AUTO_INCREMENT PRIMARY KEY,
    analyzer_id VARCHAR(20) NOT NULL,
    analyte_name VARCHAR(50) NOT NULL,
    calib_datetime DATETIME NOT NULL,
    slope DECIMAL(10,4),
    intercept DECIMAL(10,4),
    comment VARCHAR(255)
);

