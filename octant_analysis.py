import streamlit as st
import pandas as pd
from data_processing import process_data
from datetime import datetime
from io import BytesIO
import base64
import requests
from urllib.parse import urlparse
import zipfile
from data_processing import process_data


def main():
    st.set_page_config(
        page_title="Octant Analysis-Trace trajectorie", layout="wide", page_icon=":bulb:")
    st.title("Octant Analysis of particle moving in 3D Space ")

    st.write("This is a web application for octant analysis, facilitates the analysis of particle trajectories in three-dimensional space. The application preprocesses input data containing time-series data and particle coordinates assigns octant IDs based on coordinate signs.")
    st.write("It provides insights into particle behavior, including total counts, predominant octants, transition counts, and longest durations in each octant. Users can upload data files, specify mod values, and visualize octant analysis results in real-time.")

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
    You can view and download a sample input file from the following link:
    [Download Sample Input File](https://drive.google.com/file/d/1lqgbOsF8Wt3vBAaVOsNSiu532fsxBlGN/view?usp=sharing)
    """)

    # Button to use the sample input file for processing
    sampleClicked = 0
    mod_value = st.number_input(
        "Enter the Mod Value for sample input: ", value=5000)
    if st.button("Use Sample Input for Processing"):
        with st.spinner(f"Processing Sample input for mod = {mod_value}"):
            sample_input_url = "https://raw.githubusercontent.com/Rajan-CE46/moneyChanger/main/octant_input.csv"
            sample_input_df = load_csv_from_url(sample_input_url)
            # Perform data processing with the sample input file
            processed_df = process_data(sample_input_df, mod_value)
            st.write(processed_df)
            download_processed_data(processed_df)

    if (sampleClicked == 0):
        # File uploader for user data
        st.header("Upload Your Data")
        uploaded_files = st.file_uploader("Upload Data File (CSV or Excel)", type=[
            "csv", "xlsx"], accept_multiple_files=True)

        if uploaded_files:
            all_files_data = []

            for idx, uploaded_file in enumerate(uploaded_files):
                mod_value_file = st.number_input(
                    f"Enter the Mod Value for File {idx+1}", value=5000, key=f"mod_value_{idx}")
                all_files_data.append((uploaded_file, mod_value_file))
            # Submit button for processing uploaded files
            if st.button("Submit"):
                processed_files = []
                for idx, (uploaded_file, mod_value_file) in enumerate(all_files_data):
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        # Load the uploaded file
                        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(
                            'csv') else pd.read_excel(uploaded_file)

                        processed_df = process_data(df, mod_value_file)
                        st.write(f'result for {uploaded_file.name}')
                        st.write(processed_df)
                        download_processed_data(processed_df)
                        processed_files.append(processed_df)

                # Create a ZIP archive of processed files
                if (len(all_files_data) > 1):
                    zip_data = create_zip_archive(processed_files)
                    st.markdown(get_download_link(zip_data, "processed_data.zip",
                                "Download All Processed Excel Data as ZIP"), unsafe_allow_html=True)
                if (len(all_files_data) > 1):
                    # Create a ZIP archive of processed CSV files
                    zip_csv_data = create_csv_zip_archive(processed_files)
                    st.markdown(get_download_link(zip_csv_data, "processed_data_csv.zip",
                                "Download All Processed CSV Data as ZIP"), unsafe_allow_html=True)


def load_csv_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(BytesIO(response.content))
        return df
    else:
        st.error(f"Failed to load CSV from URL: {url}")
        return None


def download_processed_data(processed_df, idx=None):
    csv_data = processed_df.to_csv(index=False).encode()
    filename = f"processed_data_{idx if idx is not None else datetime.now()}.csv"
    st.markdown(get_download_link(csv_data, filename,
                f"Download Processed Data {'' if idx is None else f'for File {idx+1}'} as CSV"), unsafe_allow_html=True)

    excel_data_buffer = BytesIO()
    processed_df.to_excel(excel_data_buffer, index=False)
    excel_data = excel_data_buffer.getvalue()
    filename = f"processed_data_{idx if idx is not None else datetime.now()}.xlsx"
    st.markdown(get_download_link(excel_data, filename,
                f"Download Processed Data {'' if idx is None else f'for File {idx+1}'} as Excel"), unsafe_allow_html=True)


def create_zip_archive(processed_files):
    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, mode='w') as zip_file:
        for idx, processed_df in enumerate(processed_files):
            excel_data = BytesIO()
            with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
                processed_df.to_excel(writer, index=False)
            filename = f"processed_data_{idx if idx is not None else datetime.now()}.xlsx"
            zip_file.writestr(filename, excel_data.getvalue())
    return zip_data.getvalue()


def create_csv_zip_archive(processed_files):
    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, mode='w') as zip_file:
        for idx, processed_df in enumerate(processed_files):
            csv_data = processed_df.to_csv(index=False).encode()
            filename = f"processed_data_{idx if idx is not None else datetime.now()}.csv"
            zip_file.writestr(filename, csv_data)
    return zip_data.getvalue()


def get_download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/zip;base64,{b64}" download="{filename}">{text}</a>'


if __name__ == "__main__":
    main()
