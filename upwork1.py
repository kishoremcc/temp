import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

url = "/home/color/Videos/upwork1/IRSFORM/1040.pdf"  # Actuall URL Replace  
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')


workbook = Workbook()
sheet = workbook.active

# User Define the field names to extract we can extend as per requirements
fields = {
    'First Name': 'input[name="first_name"]',
    'Middle Initial': 'input[name="middle_initial"]',
    'Last Name': 'input[name="last_name"]',
    'Social Security Number': 'input[name="ssn"]',
    'Spouse First Name': 'input[name="spouse_first_name"]',
    'Spouse Middle Initial': 'input[name="spouse_middle_initial"]',
    'Spouse Last Name': 'input[name="spouse_last_name"]',
    'Spouse Social Security Number': 'input[name="spouse_ssn"]',
    'Home Address': 'input[name="address"]',
    'Apartment Number': 'input[name="apt_number"]',
    'City': 'input[name="city"]',
    'State': 'input[name="state"]',
    'ZIP Code': 'input[name="zip_code"]',
    'Foreign Country': 'input[name="foreign_country"]',
    'Foreign Province/State/County': 'input[name="foreign_province"]',
    'Foreign Postal Code': 'input[name="foreign_postal_code"]'
}

# Data stored with heading and user provided data corresponding
for field_name, selector in fields.items():
    field_element = soup.select_one(selector)
    field_value = field_element.get('value') if field_element else None
    sheet.append([field_name, field_value])

# store data
workbook.save('data.xlsx')

