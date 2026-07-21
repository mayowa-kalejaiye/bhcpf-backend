import pandas as pd
import sys

file_path = "Compilation of BHCPF federal and State Wards.xlsx"

try:
    xls = pd.ExcelFile(file_path)
    print(f"Found {len(xls.sheet_names)} sheets: {xls.sheet_names}\n")
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        print(f"--- Sheet: {sheet} ---")
        print(f"Columns: {list(df.columns)}")
        print(df.head(2).to_string())
        print("\n")
        
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)
