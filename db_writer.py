import pandas as pd
import mysql.connector
import os
import math

def get_latest_date():
    if not os.path.exists("data"):
        return None
    files = os.listdir("data")
    dates = []
    for f in files:
        if f.startswith("processed_fda_events_") and f.endswith(".csv"):
            date_part = f[len("processed_fda_events_"):-len(".csv")]
            dates.append(date_part)
    if not dates:
        return None
    return sorted(dates)[-1]

def clean_value(v):
    # Converts NaN (float or string) to None for SQL NULL
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, str) and v.lower() == "nan":
        return None
    return v

def insert_into_mysql(csv_path: str):
    df = pd.read_csv(csv_path)

    # Replace NaN with None (optional, but we do it in clean_value too)
    df = df.where(pd.notnull(df), None)

    # Update with your actual MySQL credentials
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="fda"
    )
    cursor = conn.cursor()

    insert_stmt = """
    INSERT INTO fda_reports
    (safetyreportid, receivedate, occurcountry, patient_age, patient_sex, drug_name, reaction, serious, seriousnessdeath)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        receivedate=VALUES(receivedate),
        occurcountry=VALUES(occurcountry),
        patient_age=VALUES(patient_age),
        patient_sex=VALUES(patient_sex),
        drug_name=VALUES(drug_name),
        reaction=VALUES(reaction),
        serious=VALUES(serious),
        seriousnessdeath=VALUES(seriousnessdeath);
    """

    for _, row in df.iterrows():
        safetyreportid = clean_value(row['safetyreportid'])
        receivedate = clean_value(row['receivedate'])
        occurcountry = clean_value(row['occurcountry'])
        patient_age = clean_value(row['patient_age'])
        patient_sex = clean_value(row['patient_sex'])
        drug_name = clean_value(row['drug_name'])
        reaction = clean_value(row['reaction'])

        serious_val = clean_value(row['serious'])
        seriousnessdeath_val = clean_value(row['seriousnessdeath'])

        # Convert serious fields to int or None
        serious_val = int(serious_val) if serious_val is not None else None
        seriousnessdeath_val = int(seriousnessdeath_val) if seriousnessdeath_val is not None else None

        data = (
            safetyreportid,
            receivedate,
            occurcountry,
            patient_age,
            patient_sex,
            drug_name,
            reaction,
            serious_val,
            seriousnessdeath_val
        )
        cursor.execute(insert_stmt, data)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {len(df)} records into the database.")

if __name__ == "__main__":
    latest_date = get_latest_date()
    if latest_date is None:
        print("❌ No processed CSV found to write into DB. Please run processor first.")
    else:
        csv_path = f"data/processed_fda_events_{latest_date}.csv"
        insert_into_mysql(csv_path)
