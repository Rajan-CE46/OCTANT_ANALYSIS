import streamlit as st
import pandas as pd
from data_processing import process_data
from datetime import datetime
from io import BytesIO
import base64
import gdown


def main():
    st.title("Octant Analysis")

    st.write("This app provides insights into octant analysis.")

    # Description of the processing tool
    st.header("Processing Tool Description")
    st.write("""
    This processing tool allows you to perform octant analysis on your data. 
    Simply upload your data files, specify the mod value, and the tool will process the data accordingly.
    """)

    # Instructions for the input file format
    st.header("Input File Format")
    st.write("""
    The input data should be provided in either CSV or Excel format. 
    Ensure that your data file contains the necessary columns and follows the required format.
    """)

    # Link to download a sample input file
    st.header("Sample Input File")
    st.write("""
    You can download a sample input file from the following link:
    [Download Sample Input File](https://drive.google.com/uc?id=1lqgbOsF8Wt3vBAaVOsNSiu532fsxBlGN)
    """)

    # Button to use the sample input file for processing
    if st.button("Use Sample Input for Processing"):
        # Load the sample input file
        # Update with the actual file path or URL
        file_id = "1lqgbOsF8Wt3vBAaVOsNSiu532fsxBlGN"
        output_path = "octant_input.csv"

        # Download the file from Google Drive
        gdown.download(
            f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)

        # Read the downloaded file into a DataFrame
        df = pd.read_csv(output_path)

        # Perform data processing with the sample input file
        mod_value = st.number_input("Enter the Mod Value", value=5000)
        processed_df = process_data(df, mod_value)

        # Display the processed data
        st.header("Processed Data")
        st.write(processed_df)

        # Download the processed data as CSV
        csv_data = processed_df.to_csv(index=False).encode()
        csv_filename = f"processed_data_{datetime.now()}.csv"
        st.markdown(get_download_link(csv_data, csv_filename,
                    "Download Processed Data as CSV"), unsafe_allow_html=True)

        # Download the processed data as Excel
        excel_data = BytesIO()
        with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
            processed_df.to_excel(writer, index=False)
        excel_filename = f"processed_data_{datetime.now()}.xlsx"
        st.markdown(get_download_link(excel_data.getvalue(), excel_filename,
                    "Download Processed Data as Excel"), unsafe_allow_html=True)

    # File uploader for user data
    st.header("Upload Your Data")
    uploaded_file = st.file_uploader(
        "Upload Data File (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        # Load the uploaded file
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(
            'csv') else pd.read_excel(uploaded_file)

        # Perform data processing
        mod_value = st.number_input("Enter the Mod Value", value=5000)
        processed_df = process_data(df, mod_value)

        # Display the processed data
        st.header("Processed Data")
        st.write(processed_df)

        # Download the processed data as CSV
        csv_data = processed_df.to_csv(index=False).encode()
        csv_filename = f"processed_data_{datetime.now()}.csv"
        st.markdown(get_download_link(csv_data, csv_filename,
                    "Download Processed Data as CSV"), unsafe_allow_html=True)

        # Download the processed data as Excel
        excel_data = BytesIO()
        with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
            processed_df.to_excel(writer, index=False)
        excel_filename = f"processed_data_{datetime.now()}.xlsx"
        st.markdown(get_download_link(excel_data.getvalue(), excel_filename,
                    "Download Processed Data as Excel"), unsafe_allow_html=True)


def get_download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


if __name__ == "__main__":
    main()
