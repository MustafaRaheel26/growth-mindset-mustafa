import streamlit as st
import pandas as pd
from io import BytesIO

# Configure Streamlit page
st.set_page_config(page_title="File Converter", layout="wide")

# Page title and description
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader: Accepts multiple CSV or Excel files
files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]  # Extract file extension
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        
        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())  # Show first few rows

        # Option to remove duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates removed successfully!")
            st.dataframe(df.head())

        # Select specific columns to keep
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart for numerical data
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])  # Show chart for first 2 numeric columns

        # File format selection for conversion
        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        # Button to download the processed file
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            
            if format_choice.lower() == "csv":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_name = file.name.replace(ext, "csv")  
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")   

            output.seek(0)
            st.download_button(
                label=f"Download {new_name}",
                data=output,
                file_name=new_name,
                mime=mime_type
            )
            st.success("Processing Completed")
