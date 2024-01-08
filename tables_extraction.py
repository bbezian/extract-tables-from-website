import streamlit as st
from urllib.request import Request, urlopen
import pandas as pd

# Function to fetch and display tables
def fetch_and_display_tables(url):
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

        # Display tables
        st.success(f"Tables found on {url}")
        for i, table in enumerate(tables, start=1):
            st.write(f"Table {i}")
            st.write(table)
            st.markdown("---")  # Add a separator between tables

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app
st.title("Web Table Extractor")

# Input URL
url = st.text_input('Enter the website URL')

# Fetch and display tables
if st.button("Fetch and Display Tables"):
    st.write(f"Fetching tables from: {url}")
    fetch_and_display_tables(url)
