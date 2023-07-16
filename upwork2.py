import PyPDF2
import pandas as pd

def extract_pdf_data(pdf_file):
    pdf_data = []
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            pdf_data.append(page.extract_text())
    return pdf_data

def save_to_excel(data, excel_file):
    df = pd.DataFrame(data, columns=['Data'])
    df.to_excel(excel_file, index=False)

# Example usage
pdf_file = '/home/color/Videos/upwork1/IRSFORM/1040.pdf'
excel_file = 'output_1040.xlsx'

pdf_data = extract_pdf_data(pdf_file)
save_to_excel(pdf_data, excel_file)

