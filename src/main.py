"""
Clinical Diagnostics Data Quality Dashboard
Beginner–Intermediate Level

This script:
1. Connects to MySQL
2. Loads lab test results, QC logs, and calibration logs
3. Detects abnormal values
4. Calculates QC pass rate
5. Checks calibration drift
6. Generates graphs and exports them into a PDF report
"""

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# ----------------------------- DATABASE CONNECTION -----------------------------

def get_connection():
    """Connect to clinical_lab database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sqlsqlsql",  
        database="clinical_lab"
    )
    return conn


# ----------------------------- LOAD DATA FROM MYSQL -----------------------------

def load_test_results():
    conn = get_connection()
    query = """
        SELECT 
            s.sample_date,
            s.analyzer_id,
            r.sample_id,
            r.analyte_name,
            r.result_value,
            r.reference_low,
            r.reference_high
        FROM test_results r
        JOIN samples s ON r.sample_id = s.sample_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Convert datetime to proper type
    df["sample_date"] = pd.to_datetime(df["sample_date"])
    return df


def load_qc_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM qc_logs;", conn)
    conn.close()

    df["run_datetime"] = pd.to_datetime(df["run_datetime"])
    return df


def load_calibration_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM calibration_logs;", conn)
    conn.close()

    df["calib_datetime"] = pd.to_datetime(df["calib_datetime"])
    return df


# ----------------------------- ANALYSIS FUNCTIONS -----------------------------

def detect_abnormal(df):
    """Flag abnormal results based on reference range."""
    df = df.copy()
    df["is_abnormal"] = (
        (df["result_value"] < df["reference_low"]) |
        (df["result_value"] > df["reference_high"])
    )
    return df


def daily_abnormal_trend(df):
    df = detect_abnormal(df)
    df["date"] = df["sample_date"].dt.date

    summary = df.groupby(["date", "analyte_name"]).agg(
        total_tests=("result_value", "count"),
        abnormal_tests=("is_abnormal", "sum")
    ).reset_index()

    summary["abnormal_pct"] = (summary["abnormal_tests"] / summary["total_tests"]) * 100
    return summary


def qc_pass_rate(df_qc):
    df_qc["date"] = df_qc["run_datetime"].dt.date

    summary = df_qc.groupby("date").agg(
        total_runs=("status", "count"),
        pass_runs=("status", lambda x: (x == "PASS").sum())
    ).reset_index()

    summary["pass_rate_pct"] = (summary["pass_runs"] / summary["total_runs"]) * 100
    return summary


def calibration_drift(df_calib):
    df = df_calib.copy()
    df["date"] = df["calib_datetime"].dt.date
    return df.sort_values(["analyzer_id", "analyte_name", "date"])


# ----------------------------- PDF REPORT GENERATION -----------------------------

def generate_pdf(results, qc, calib):
    with PdfPages("../reports/lab_daily_report.pdf") as pdf:

        # 1. Abnormal values per analyte
        abnormal_summary = daily_abnormal_trend(results)

        fig1, ax1 = plt.subplots()
        abnormal_summary.groupby("analyte_name")["abnormal_pct"].mean().plot(kind="bar", ax=ax1)
        ax1.set_title("Average % Abnormal Results per Analyte")
        ax1.set_ylabel("% Abnormal")
        pdf.savefig(fig1)
        plt.close(fig1)

        # 2. QC Pass Rate Trend
        qc_summary = qc_pass_rate(qc)

        fig2, ax2 = plt.subplots()
        ax2.plot(qc_summary["date"], qc_summary["pass_rate_pct"], marker="o")
        ax2.set_title("QC Pass Rate Over Time")
        ax2.set_ylabel("Pass Rate (%)")
        ax2.set_xlabel("Date")
        pdf.savefig(fig2)
        plt.close(fig2)

        # 3. Calibration Drift
        calib_summary = calibration_drift(calib)

        fig3, ax3 = plt.subplots()
        for (analyzer, analyte), subset in calib_summary.groupby(["analyzer_id", "analyte_name"]):
            ax3.plot(subset["date"], subset["slope"], marker="o", label=f"{analyzer}-{analyte}")
        ax3.set_title("Calibration Slope Drift Over Time")
        ax3.set_ylabel("Slope")
        ax3.legend()
        pdf.savefig(fig3)
        plt.close(fig3)

    print("📄 PDF Report saved at: reports/lab_daily_report.pdf")


# ------------------------------------ MAIN -------------------------------------

def main():
    print("Loading data from MySQL...")

    results = load_test_results()
    qc = load_qc_logs()
    calib = load_calibration_logs()

    print("Sample Data:")
    print(results.head())

    print("\nGenerating PDF Dashboard...")
    generate_pdf(results, qc, calib)

    print("Done!")


if __name__ == "__main__":
    main()
