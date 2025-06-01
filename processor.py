import json
import pandas as pd
import os

SEX_MAP = {"1": "Male", "2": "Female", "0": "Unknown"}

def try_float(value):
    try:
        return float(value)
    except:
        return None

def extract_events(json_path: str) -> str:
    with open(json_path, "r") as f:
        data = json.load(f)

    rows = []
    for event in data.get("results", []):
        patient = event.get("patient", {})
        drugs = patient.get("drug", [])
        reactions = patient.get("reaction", [])

        row = {
            "safetyreportid": event.get("safetyreportid"),
            "receivedate": event.get("receivedate"),
            "occurcountry": event.get("occurcountry"),
            "patient_age": try_float(patient.get("patientonsetage")),
            "patient_sex": SEX_MAP.get(str(patient.get("patientsex")), "Unknown"),
            "drug_name": "; ".join(d.get("medicinalproduct", "") for d in drugs),
            "reaction": "; ".join(r.get("reactionmeddrapt", "") for r in reactions),
            "serious": int(event.get("serious", 0)),
            "seriousnessdeath": int(event.get("seriousnessdeath", 0))
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    print(f"✅ Processed {len(df)} records.")
    
    today = json_path.split("_")[-1].split(".")[0]
    processed_path = f"data/processed_fda_events_{today}.csv"
    df.to_csv(processed_path, index=False)
    print(f"📄 Saved processed CSV to {processed_path}")
    return processed_path

def get_latest_raw_date():
    if not os.path.exists("data"):
        return None
    files = os.listdir("data")
    dates = []
    for f in files:
        if f.startswith("raw_fda_") and f.endswith(".json"):
            date_part = f[len("raw_fda_"):-len(".json")]
            dates.append(date_part)
    if not dates:
        return None
    return sorted(dates)[-1]


if __name__ == "__main__":
    latest_date = get_latest_raw_date()
    if latest_date is None:
        print("❌ No raw JSON data found to process. Please run downloader first.")
    else:
        json_path = f"data/raw_fda_{latest_date}.json"
        extract_events(json_path)

