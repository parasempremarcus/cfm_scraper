# 🤖 CFM Scraper
<img src="img/cfm_crms.png" alt="CFM Logo" width="600"/>

A web scraper of the database made publicly available by the Federal Council of Medicine (CFM)

## Context 🕵️‍♂️
CFM Scraper is a Python-based web scraper designed to extract valuable information from the publicly available database of the Federal Council of Medicine (Conselho Federal de Medicina, CFM) in Brazil. The CFM oversees professional regulations and licensing for medical practitioners nationwide.

The CFM website provides access to a comprehensive database containing crucial details about all registered doctors in Brazil, including their registration number (CRM), primary and secondary states of practice, specialty, graduation date, and other pertinent data. However, due to the lack of an official API and the sheer volume of data, extracting information for in-depth analysis becomes challenging using the council's search interface alone.

This project aims to facilitate data extraction by providing a web scraping solution that exports the collected information into an Excel spreadsheet or a CSV file.

## Usage 🚀
### `project.py`

To use the scraper effectively, the user needs to provide the following filters:
1. Brazilian state for data collection (in Portuguese, e.g., Rio de Janeiro)
2. Specialty of doctors (e.g., Neurocirurgia)
3. Type of registration (Principal, Secundária, or Provisória)
4. Situation of registration (Ativo or Inativo)

The main objectives of the program include extracting the doctor's CRM, name, type of registration, and registration status. Key packages utilized in this project are:
- **Selenium** 🌐: Main package for web scraping
- **Pandas** 🐼: Used for data manipulation and storage
- **alive-bar** 🔄: Implements a progress bar in the terminal
- **time** ⏰: Provides cooldown between Selenium processes
- **openpyxl** 📊: A Pandas helper for exporting data to Excel

The program initiates by opening the Chrome browser, accepting cookies, and prompting the user to input the desired filters using the `coletar()` function. Subsequently, these filters are applied on the website through the `preencher()` function, initiating the search process. In case of a Google Recaptcha challenge, the `anti_recaptcha()` function is invoked within `preencher()` to handle it.

If no Recaptcha appears, the program proceeds with the `scrape()` function, which collects the data based on the user's specified filters. If a Recaptcha does appear, the `anti_recapcha()` function resolves it before continuing with `scrape()`.

Once the data is collected and stored in a list with a dictionary for each doctor, the `selecionar_formato()` function is called. This function prompts the user to choose the desired format for exporting the data: calling `extrair_excel()` for Excel or `extrair_csv()` for CSV, thereby generating the respective file.

### `miscellaneous.py`
This file stores all the lists and dictionaries essential for the program's proper execution, contributing to the readability of `project.py`.

### `test_project.py`
Due to the nature of most functions running in the browser, only three functions are suitable for testing using pytest: `selecionar_formato()`, `exportar_csv()`, and `exportar_excel()`. These functions ensure that the core functionality of the program is validated through testing.
