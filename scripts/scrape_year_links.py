from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

# Load page
url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)
time.sleep(2)

# Find all <a> elements inside the <ul> that contains the yearly links
year_links = driver.find_elements(
    By.XPATH,  '//table//a')

data = []
for link in year_links:
    year = link.text.strip()
    href = link.get_attribute('href')

    if year.isdigit():
        data.append({
            "Year": year,
            "URL": href
        })

# Create data folder and save results
os.makedirs("data", exist_ok=True)

if data:
    df = pd.DataFrame(data)
    df.to_csv("data/mlb_year_links.csv", index=False)
    print(f"Saved {len(df)} year links to data/mlb_year_links.csv")
else:
    print("x - No data found. Please check the selectors or page load.")

driver.quit()
