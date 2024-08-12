import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
import pandas as pd
import os
import io

# Function to extract and save PDF pages with account numbers
def extract_and_save_pdfs(file_path, output_folder, df):
    inputpdf = PdfReader(open(file_path, "rb"))
    extracted_numbers = []
    for Pin, i in zip(df['Property Account No'], range(len(inputpdf.pages))):
        output = PdfWriter()
        output.add_page(inputpdf.pages[i])
        
        # Replace semicolons (:) and hyphens (-) with underscores (_)
        sanitized_name = Pin.replace(':', '_').replace('-', '_')
        acc_num = f'{sanitized_name}_Mail Out'
        output_file_path = os.path.join(output_folder, f"{acc_num}.pdf")
        
        with open(output_file_path, "wb") as outputStream:
            output.write(outputStream)
        
        extracted_numbers.append(acc_num)
    return extracted_numbers

# Main function to run the Streamlit app
def main():
    st.title("PDF Splitter and Renamer")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    # Upload Excel file
    excel_file = st.file_uploader("Upload Excel file", type=["csv", "xlsx"])

    if pdf_file and excel_file:
        # User-specified output folder
        output_folder = st.text_input("Enter the output folder path:", r'Hotel Extraction Path')
        
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
            st.write("Extracting and saving PDF files...")
            
            # Saving the uploaded PDF file
            file_path = os.path.join(output_folder, "temp_file.pdf")
            with open(file_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            # Reading the Excel file
            if excel_file.name.endswith('.csv'):
                df = pd.read_csv(excel_file)
            else:
                df = pd.read_excel(io.BytesIO(excel_file.getvalue()))
            
            # Extract and save the PDF pages
            extracted_numbers = extract_and_save_pdfs(file_path, output_folder, df)
            
            st.write("Extracted and saved the following PDF files:")
            for number in extracted_numbers:
                st.write(number)
            
            st.success("PDF files have been processed and saved successfully.")

if __name__ == "__main__":
    main()
