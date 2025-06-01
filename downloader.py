import requests
import datetime
import os

def download_fda_data(start_date_str="20230701"):
    start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d").date()
    today = datetime.date.today()
    
    date_to_try = start_date
    
    while date_to_try <= today:
        date_str = date_to_try.strftime("%Y%m%d")
        print(f"📡 Fetching data for date: {date_str}")
        
        url = f"https://api.fda.gov/drug/event.json?search=receivedate:[{date_str}+TO+{date_str}]&limit=100"
        response = requests.get(url)
        
        if response.status_code == 200:
            if '"results"' in response.text:  # basic check to confirm data exists
                os.makedirs("data", exist_ok=True)
                file_path = f"data/raw_fda_{date_str}.json"
                with open(file_path, "w") as f:
                    f.write(response.text)
                print(f"✅ Data downloaded and saved to {file_path}")
                return date_str
            else:
                print(f"❌ No data for {date_str}")
        else:
            print(f"❌ Failed ({response.status_code}) on {date_str}")
        
        date_to_try += datetime.timedelta(days=1)
    
    print("❌ No data found from start date to today.")
    return None

def get_latest_date():
    # This function will find the latest downloaded date file in data folder
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
    download_fda_data()
