from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Start WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

# List to store all extracted data
all_data = []

try:
    # Step 1: Open the main URL
    driver.get("https://samadhaan.msme.gov.in/MyMsme/MSEFC/MSEFC_Welcome.aspx")

    # Step 2: Click "More Info"
    wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_lblCaseMoreRpt30"))).click()

    # Step 3: Click "1549"
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="example1"]/tbody[1]/tr[1]/td[11]/a'))).click()

    # Step 4: Click "335"
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rptRecord_ctl09_NotResponseCol"]/a'))).click()

    # Wait for the table and dropdown to load
    wait.until(EC.presence_of_element_located((By.ID, "example1_length")))
    time.sleep(2)  # small pause to ensure table is fully loaded

    # Step 5: Select "All" from the dropdown to show all entries
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="example1_length"]/label/select')))
    select = Select(select_element)
    select.select_by_value('-1')  # Select "All"

    # Wait for table to reload after selecting "All"
    time.sleep(5)  # Adjust if needed

    # Step 6: Extract all "View" links again (now for all entries)
    view_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@id, "application_view")]')))
    total_links = len(view_links)
    print(f"Total View links found after selecting All: {total_links}")

    for i in range(total_links):
        # Refetch the view links each time because DOM refreshes
        view_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@id, "application_view")]')))
        driver.execute_script("arguments[0].scrollIntoView();", view_links[i])

        # Click on the view link
        view_links[i].click()

        # Wait for detail table to load
        time.sleep(3)

        # Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="table table-bordered")

        data = {}

        def get_td_text(tr, index):
            tds = tr.find_all("td")
            return tds[index].get_text(strip=True) if len(tds) > index else ""

        rows = table.find_all("tr")

        # Extract data fields safely
        if len(rows) >= 10:
            data["Application/Temp No."] = get_td_text(rows[1], 1)
            data["Date of Filing Application"] = get_td_text(rows[1], 4)
            data["Name of Petitioner"] = get_td_text(rows[2], 1)
            data["Name of Petitioner Unit"] = get_td_text(rows[2], 3)
            data["State of Petitioner"] = get_td_text(rows[2], 5)
            data["District of Petitioner"] = get_td_text(rows[3], 1)
            data["Name of Respondent"] = get_td_text(rows[5], 1)
            data["State of Respondent"] = get_td_text(rows[5], 3)
            data["District of Respondent"] = get_td_text(rows[5], 5)
            data["Respondent Category"] = get_td_text(rows[6], 1)
            data["Principal Amount Payable"] = get_td_text(rows[6], 3)
            data["Case Status"] = get_td_text(rows[6], 5)
            data["Work Order Detail"] = get_td_text(rows[8], 1)
            data["Work Order Date"] = get_td_text(rows[8], 5)
            data["Invoice Detail"] = get_td_text(rows[9], 1)
            data["Invoice Date"] = get_td_text(rows[9], 5)
        else:
            print(f"Unexpected table format for entry {i+1}")

        all_data.append(data)

        # Go back to the previous page with the full table
        driver.back()
        time.sleep(5)

        # Re-select "All" again after coming back to keep showing all entries
        select_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="example1_length"]/label/select')))
        select = Select(select_element)
        select.select_by_value('-1')
        time.sleep(5)

    # Convert all data to DataFrame and save
    df = pd.DataFrame(all_data)
    df.to_excel("Ministry of coal.xlsx", index=False)
    print("All data saved to All_View_Data_Full.xlsx")

finally:
    driver.quit()


