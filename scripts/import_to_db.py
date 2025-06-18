import sqlite3
import pandas as pd
import os

# Input CSV files and destination database path
csv_files = {
    "year_links": "data/mlb_year_links.csv",
    "year_details": "data/mlb_year_details.csv"
}
db_path = "db/mlb_history.db"

# Ensure the db/ folder exists
os.makedirs("db", exist_ok=True)

# Connect to SQLite (it will create the file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for table_name, csv_path in csv_files.items():
    try:
        print(f"Importing {csv_path} into table `{table_name}`")

        # Load CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Infer types & import into SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"Imported {len(df)} rows into `{table_name}`")
    except Exception as e:
        print(f"x- Failed to import {csv_path}: {e}")

# Close connection
conn.close()
print("Database import complete.")
