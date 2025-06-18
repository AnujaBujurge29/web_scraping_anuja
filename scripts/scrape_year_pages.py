import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

# Load the year links from CSV
links_df = pd.read_csv("data/mlb_year_links.csv")

# Output list
all_data = []

# Loop through each year and URL
for idx, row in links_df.iterrows():
    year = row["Year"]
    url = row["URL"]
    print(f"Scraping year {year}...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all <p> tags as historical details
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                all_data.append({
                    "Year": year,
                    "Detail": text
                })

        time.sleep(0.5)  # Be polite to the server

    except Exception as e:
        print(f"Error scraping {year}: {e}")
        continue

# Save to CSV
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(all_data)
df.to_csv("data/mlb_year_details.csv", index=False)
print(f"Saved {len(df)} rows to data/mlb_year_details.csv")
