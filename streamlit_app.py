import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
import os
import pandas as pd
import io

def extract_account_numbers(file_path, output_folder, df):
    """
    Extracts account numbers from the PDF file and saves each page with a name based on account numbers.

    Args:
        file_path (str): Path to the input PDF file.
        output_folder (str): Folder to save the extracted PDF files.
        df (pd.DataFrame): DataFrame containing account numbers.

    Returns:
        list: List of extracted account numbers.
    """
    inputpdf = PdfReader(open(file_path, "rb"))
    extracted_numbers = []
    for Pin, i in zip(df['Property Account No'], range(len(inputpdf.pages))):
        output = PdfWriter()
        output.add_page(inputpdf.pages[i])
        acc_num = f'{Pin}_Mail_Out'
        # Sanitize file name
        acc_num = acc_num.replace(':', '_').replace('-', '_')
        output_file_path = os.path.join(output_folder, f"{acc_num}.pdf")
        with open(output_file_path, "wb") as outputStream:
            output.write(outputStream)
        extracted_numbers.append(acc_num)
    return extracted_numbers

def main():
    st.title("PDF Account Number Extraction")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    # Upload Excel or CSV file
    uploaded_data = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])

    # Input for output folder
    output_folder = st.text_input("Specify output folder path", "Hotel Extraction Path")
    
    if uploaded_file is not None and uploaded_data is not None:
        if not os.path.isabs(output_folder):
            # Make output folder path absolute
            output_folder = os.path.join(os.getcwd(), output_folder)
        
        os.makedirs(output_folder, exist_ok=True)
        
        st.write("Extracting account numbers...")
        
        # Save the uploaded PDF file
        file_path = os.path.join(output_folder, "temp_file.pdf")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read the uploaded data
        data = io.BytesIO(uploaded_data.getvalue())
        df = pd.read_excel(data)  # Assuming uploaded file is in Excel format
        
        # Extract account numbers and save files
        extracted_numbers = extract_account_numbers(file_path, output_folder, df)
        
        st.write("Extracted Account Numbers:")
        for number in extracted_numbers:
            st.write(number)
        
        st.write(f"Files have been saved in: {output_folder}")

if __name__ == "__main__":
    main()

