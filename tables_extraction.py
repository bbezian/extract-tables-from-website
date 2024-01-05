import streamlit as st
from urllib.request import Request, urlopen
import pandas as pd
import os
import zipfile

# Function to fetch and save tables
def fetch_and_save_tables(url, loc):
    try:
        # Check if the URL is not empty
        if not url:
            st.warning("Please enter a valid URL.")
            return

        # Write the code for calling the website
        request = Request(url)
        request.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')

        # Fetch the HTML content
        with urlopen(request) as page:
            html_content = page.read()

        # Read tables from HTML content
        tables = pd.read_html(html_content)

        if not tables:
            st.warning("No tables found on the page.")
            return

        # Save each table as a separate CSV file
        zip_filename = os.path.join(loc, 'tables.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for i, table in enumerate(tables, start=1):
                file_name = f'table_{i}.csv'
                file_path = os.path.join(loc, file_name)
                table.to_csv(file_path, index=False)
                zip_file.write(file_path, file_name)

                st.success(f"Table {i} saved as {file_path}")
                st.write(table)

        st.success(f"All tables saved successfully. Click the button below to download.")
        return zip_filename

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
st.title("Web Table Extractor")

# Input URL
url = st.text_input('Enter the website URL')

# Input directory (in the sidebar)
loc = st.sidebar.text_input('Enter the directory to save CSV files', os.path.expanduser("~"))

# Fetch and save tables
if st.button("Fetch and Save Tables"):
    st.write(f"Fetching tables from: {url}")
    if loc:
        zip_filename = fetch_and_save_tables(url, loc)
    else:
        st.warning("Please enter a directory to save the CSV files.")

# Download button
if 'zip_filename' in locals():
    st.download_button(
        label="Download Tables as ZIP",
        key="download_button",
        on_click=None,
        args=(zip_filename,),
        help="Click to download the tables as a ZIP file.",
    )
