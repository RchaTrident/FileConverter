import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import  auth
from io import BytesIO
import converter
import json


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        auth.login_page()
        return
    
    uploaded_file = st.file_uploader("Choose a file")
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
            filename = uploaded_file.name
            dataframe = pd.read_excel(uploaded_file, sheet_name=None)
            st.session_state['output_data'] = converter.convert_bay_data(dataframe)
            st.write(st.session_state['output_data'])
            month = st.date_input("Month")
            if st.button("Offshore"):
                output_filename = f"BPCO_{month}.json"
                towrite = BytesIO()
                towrite.write(json.dumps(st.session_state['output_data']).encode())
                towrite.seek(0)
                st.download_button(
                    label="Download Offshore results",
                    data=towrite,
                    file_name=output_filename,
                    mime="application/json"
                )
            
            if st.button("Fund"):
                fund_code = st.selectbox("Fund Number", ["II", "I"])
                output_filename = f"BPC{fund_code}_{month}.json"
                towrite = BytesIO()
                towrite.write(json.dumps(st.session_state['output_data']).encode())
                towrite.seek(0)
                
                st.download_button(
                    label="Download Fund results",
                    data=towrite,
                    file_name=output_filename,
                    mime="application/json"
                )
        else:
            st.write("Please upload an Excel file.")
    else:
        st.write("No file uploaded yet.")

if __name__ == "__main__":
    main()