USE clinical_lab;

-- Patients
INSERT INTO patients (patient_code, sex, dob) VALUES
('PT001', 'F', '1995-02-14'),
('PT002', 'M', '1988-11-22'),
('PT003', 'F', '2001-04-10');

-- Samples
INSERT INTO samples (patient_id, sample_date, sample_type, analyzer_id) VALUES
(1, '2025-01-01 08:30:00', 'Serum', 'Analyzer_A'),
(2, '2025-01-01 09:10:00', 'Serum', 'Analyzer_A'),
(3, '2025-01-02 10:05:00', 'Serum', 'Analyzer_B');

-- Test results for 3 analytes (Glucose, Urea, Creatinine)
-- Ref ranges:
-- Glucose: 70-110, Urea: 15-40, Creatinine: 0.6-1.3

INSERT INTO test_results (sample_id, analyte_name, result_value, unit, reference_low, reference_high) VALUES
(1, 'Glucose', 95, 'mg/dL', 70, 110),
(1, 'Urea', 20, 'mg/dL', 15, 40),
(1, 'Creatinine', 0.9, 'mg/dL', 0.6, 1.3),

(2, 'Glucose', 145, 'mg/dL', 70, 110),   -- high
(2, 'Urea', 38, 'mg/dL', 15, 40),
(2, 'Creatinine', 1.0, 'mg/dL', 0.6, 1.3),

(3, 'Glucose', 85, 'mg/dL', 70, 110),
(3, 'Urea', 50, 'mg/dL', 15, 40),        -- high
(3, 'Creatinine', 1.5, 'mg/dL', 0.6, 1.3); -- high

-- QC logs
INSERT INTO qc_logs (run_datetime, analyte_name, level, qc_value, target_value, sd, status) VALUES
('2025-01-01 07:00:00', 'Glucose', 'L1', 100, 100, 2, 'PASS'),
('2025-01-01 07:00:00', 'Urea', 'L1', 45, 35, 3, 'FAIL'),
('2025-01-02 07:00:00', 'Creatinine', 'L1', 1.0, 0.9, 0.2, 'PASS');

-- Calibration logs
INSERT INTO calibration_logs (analyzer_id, analyte_name, calib_datetime, slope, intercept, comment) VALUES
('Analyzer_A', 'Glucose', '2024-12-28 06:40:00', 1.01, 0.10, 'Stable'),
('Analyzer_A', 'Glucose', '2025-01-02 06:40:00', 1.08, 0.15, 'Slight drift'),
('Analyzer_B', 'Creatinine', '2025-01-02 06:40:00', 1.12, 0.20, 'Drift suspected');
USE clinical_lab;
SELECT * FROM test_results;
SELECT * FROM qc_logs;
SELECT * FROM calibration_logs;