import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
import os
import pandas as pd
import io

def extract_and_rename_pdfs(pdf_reader, output_folder, df):
    extracted_numbers = []
    for account_number, i in zip(df['Property Account No'], range(len(pdf_reader.pages))):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[i])
        
        # Replace semicolons (:) and hyphens (-) with underscores (_)
        sanitized_account_number = account_number.replace(':', '_').replace('-', '_')
        output_filename = f'{sanitized_account_number}_Mail_Out.pdf'
        output_file_path = os.path.join(output_folder, output_filename)
        
        with open(output_file_path, "wb") as outputStream:
            pdf_writer.write(outputStream)
        extracted_numbers.append(output_filename)
    return extracted_numbers

def main():
    st.title("PDF Splitter and Renamer")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Upload Excel file
    excel_file = st.file_uploader("Upload an Excel file", type=["csv", "xlsx"])

    # User specifies the output folder path
    output_folder = st.text_input("Specify the output folder path", r'Hotel Extraction Path')

    if pdf_file and excel_file and output_folder:
        os.makedirs(output_folder, exist_ok=True)
        st.write("Processing the files...")

        # Read the uploaded PDF file
        pdf_reader = PdfReader(pdf_file)

        # Read the uploaded Excel file
        if excel_file.name.endswith('.csv'):
            df = pd.read_csv(excel_file)
        else:
            df = pd.read_excel(excel_file)

        # Check if the number of pages matches the number of account numbers
        if len(pdf_reader.pages) != len(df):
            st.error("The number of pages in the PDF does not match the number of rows in the Excel file.")
        else:
            extracted_numbers = extract_and_rename_pdfs(pdf_reader, output_folder, df)
            st.success(f"PDFs have been split and renamed successfully. Files are saved in: {output_folder}")
            st.write("Extracted and renamed files:")
            for filename in extracted_numbers:
                st.write(filename)

if __name__ == "__main__":
    main()

