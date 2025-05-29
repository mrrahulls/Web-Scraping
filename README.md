# Web-Scraping
# roject Title:
# Automated Web Scraping of MSME Case Details from Government Portal

# Key Highlights:
🔍 Automated Web Navigation: Used Selenium WebDriver to automate interaction with the MSME Samadhaan portal, navigating through multiple layers of links and tables.

⏳ Dynamic Content Handling: Employed WebDriverWait and ExpectedConditions to ensure stability while waiting for dynamically loaded elements.

🧾 Dropdown Interaction: Programmatically selected "Show All" from a dropdown to extract all visible records in one view.

🔗 Iterative Link Clicking: Automatically looped through and clicked each "View" link to access detailed case information.

🥣 Data Extraction with BeautifulSoup: Parsed case details using BeautifulSoup to extract structured data from HTML tables.

📄 Robust Data Collection: Extracted fields such as Application No., Filing Date, Petitioner/Respondent details, Amounts, and Case Status.

📦 Data Storage: Compiled all extracted records into a Pandas DataFrame and saved it to an Excel file for further analysis.

🔁 Session Management: Maintained page state after each extraction using Selenium’s navigation and dropdown reselection.

🧠 Error Handling: Included checks to handle unexpected table formats and avoid script crashes.
