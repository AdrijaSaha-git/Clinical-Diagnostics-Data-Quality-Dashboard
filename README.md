# Clinical Diagnostics Data Quality Dashboard

This project simulates a clinical diagnostics lab environment and focuses on **data quality monitoring** using Python and MySQL.

It mirrors real laboratory workflows such as sample processing, QC checks, calibration review, and LIS-style documentation.

## Project Objectives 💻

- Store **patient samples, test results, QC logs, and calibration data** in a MySQL database  
- Use **Python** to:
  - Detect outliers in biochemical analytes
  - Track daily QC pass/fail rates
  - Identify analyzer drift over time based on calibration logs
- Build simple dashboards and plots for:
  - Trends in abnormal values
  - Daily QC summary
- Export **automated daily PDF data quality reports**

## Tech Stack 🛠

- **Language:** Python  
- **Database:** MySQL  
- **Libraries:** pandas, matplotlib, mysql-connector-python, reportlab / matplotlib PdfPages  


