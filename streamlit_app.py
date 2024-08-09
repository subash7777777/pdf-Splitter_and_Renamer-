import streamlit as st
import PyPDF2
import pandas as pd
import zipfile
import os
import math

# Streamlit app title
st.title("PDF Splitter and Renamer")

# Upload PDF file
pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

# Upload Excel file
excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if pdf_file and excel_file:
    # Read the Excel file
    names_df = pd.read_excel(excel_file)
    names_list = names_df.iloc[:, 0].tolist()  # Assuming names are in the first column

    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Check if the number of pages matches the number of names
    if len(pdf_reader.pages) != len(names_list):
        st.error("The number of pages in the PDF does not match the number of names in the Excel file.")
    else:
        # Create a directory to save the split PDF files
        output_dir = "split_pdfs"
        os.makedirs(output_dir, exist_ok=True)

        # Split and save each page with the respective name
        for i, page in enumerate(pdf_reader.pages):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(page)
            
            output_filename = f"{names_list[i]}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
        
        # Split the ZIP file into chunks (e.g., 100 MB per chunk)
        def create_zip_files(directory, chunk_size_mb=100):
            chunk_size = chunk_size_mb * 1024 * 1024  # Convert to bytes
            zip_counter = 1
            zip_filename = f"split_pdfs_part_{zip_counter}.zip"
            zipf = zipfile.ZipFile(zip_filename, 'w')
            total_size = 0
            
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                total_size += os.path.getsize(file_path)
                
                if total_size > chunk_size:
                    zipf.close()
                    zip_counter += 1
                    zip_filename = f"split_pdfs_part_{zip_counter}.zip"
                    zipf = zipfile.ZipFile(zip_filename, 'w')
                    total_size = os.path.getsize(file_path)
                
                zipf.write(file_path, file)
            zipf.close()
            return zip_counter

        # Create the ZIP files
        total_parts = create_zip_files(output_dir)

        # Provide download buttons for each part
        for part in range(1, total_parts + 1):
            part_filename = f"split_pdfs_part_{part}.zip"
            with open(part_filename, "rb") as f:
                st.download_button(
                    label=f"Download ZIP Part {part}",
                    data=f,
                    file_name=part_filename,
                    mime="application/zip"
                )

        st.success("PDF has been split, renamed, and zipped successfully. Click the buttons above to download the files.")

