import os
import json
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables, overriding any cached ones
load_dotenv(override=True)

url_raw = os.environ.get("SUPABASE_URL")
key_raw = os.environ.get("SUPABASE_KEY")

url: str = url_raw.strip() if url_raw else None
key: str = key_raw.strip() if key_raw else None

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in your .env file")
    exit(1)

supabase: Client = create_client(url, key)

def seed_benefits():
    print("Seeding benefits from JSON...")
    try:
        with open("backend/data/bhcpf_benefits.json", "r") as f:
            data = json.load(f)
            
        services = data.get("services", [])
        if not services:
            print("No services found in JSON.")
            return

        for idx, item in enumerate(services):
            record = {
                "service": item.get("service"),
                "category": item.get("category"),
                "level": item.get("level"),
                "details": item.get("details"),
                "limits": item.get("limits"),
                "access_point": item.get("access_point")
            }
            # Use upsert or just insert
            response = supabase.table("benefits").insert(record).execute()
            print(f"Inserted benefit {idx+1}/{len(services)}: {item.get('service')}")
            
    except Exception as e:
        print(f"Failed to seed benefits: {e}")


def seed_facilities():
    file_path = "Compilation of BHCPF federal and State Wards.xlsx"
    print(f"Seeding facilities from {file_path}...")
    try:
        xls = pd.ExcelFile(file_path)
        all_facilities = []
        
        for sheet_name in xls.sheet_names:
            # Read with header=1 because row 0 contains the actual column names
            df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
            
            # Forward fill LGA just in case there are merged cells/blanks
            # Ensure we find the column names dynamically (ignoring case/spaces)
            col_map = {c.strip().lower(): c for c in df.columns if isinstance(c, str)}
            
            lga_col = col_map.get("lga")
            ward_col = col_map.get("federal ward")
            facility_col = col_map.get("health facilities")
            
            if not lga_col or not ward_col or not facility_col:
                print(f"Skipping sheet {sheet_name} due to missing core columns. Found: {list(df.columns)}")
                continue
                
            # Drop empty rows where facility name is missing
            df = df.dropna(subset=[facility_col])
            
            # Forward fill LGA and Ward
            df[lga_col] = df[lga_col].ffill()
            df[ward_col] = df[ward_col].ffill()
            
            for _, row in df.iterrows():
                lga = str(row[lga_col]).strip()
                ward = str(row[ward_col]).strip()
                facilities_raw = str(row[facility_col]).strip()
                
                # Some facilities are comma separated in the same cell
                for fac in facilities_raw.split(','):
                    fac = fac.strip()
                    if fac and fac.lower() != 'nan':
                        # Standardize naming e.g., "Phc" to "PHC"
                        if fac.lower().startswith('phc'):
                            fac = "PHC" + fac[3:]
                        
                        all_facilities.append({
                            "facility_name": fac,
                            "lga": lga,
                            "ward": ward,
                            "state": "Plateau"
                        })
                        
        print(f"Found {len(all_facilities)} clean facilities across all sheets.")
        
        # Insert in chunks to avoid payload too large errors
        chunk_size = 100
        for i in range(0, len(all_facilities), chunk_size):
            chunk = all_facilities[i:i+chunk_size]
            supabase.table("facilities").insert(chunk).execute()
            print(f"Inserted facilities {i} to {i+len(chunk)}")
            
        print("Facilities seeding completed successfully!")

    except Exception as e:
        print(f"Failed to seed facilities: {e}")

if __name__ == "__main__":
    print("Starting DB Seed Process...")
    seed_benefits()
    seed_facilities()
    print("Done!")
