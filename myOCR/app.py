import streamlit as st
import ocrmypdf
import os
import tempfile
from pathlib import Path

st.title("📄 PDF OCR Converter")
st.write("Upload a PDF, and I will add a text layer to it using OCR.")

# File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary directory to handle the files securely
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Define paths for input and output files inside the temp folder
        input_path = os.path.join(temp_dir, "input.pdf")
        output_path = os.path.join(temp_dir, "output_ocr.pdf")
        
        # Save the uploaded file to the temp input path
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info("Processing... This may take a moment depending on file size.")
        
        try:
            # Run the OCR command
            # skip_text=True keeps existing text and only OCRs images
            ocrmypdf.ocr(input_path, output_path, skip_text=True, deskew=True)
            
            st.success("OCR Complete!")
            
            # Read the processed file back into memory to let the user download it
            with open(output_path, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                label="Download OCR'd PDF",
                data=pdf_bytes,
                file_name="ocr_processed_document.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            
    # Once we exit the 'with tempfile...' block, the folder and files are auto-deleted.
