import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import database, auth
from io import BytesIO
import converter
import converterOffshore

@st.cache_resource
def get_snowflake_connection():
    return database.get_snowflake_connection()

@st.cache_data
def load_data(query, params=None):
    conn = get_snowflake_connection()
    return pd.read_sql(query, conn, params=params)

def reset_session_state(except_keys):
    for key in list(st.session_state.keys()):
        if key not in except_keys:
            del st.session_state[key]

def prettify_name(name):
    """Converts a string like 'customer_transactions_parallaxes_capital_llc' to 'Parallaxes Capital LLC'."""
    words = name.split('_')
    pretty_name = ' '.join(word.capitalize() for word in words)
    return pretty_name

def get_last_day_of_month(month):
    """Returns the last day of the given month in the current year."""
    year = datetime.now().year
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)
    return last_day.day

def main():
    conn = get_snowflake_connection()
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
            output_data = converter.convert_bay_data(dataframe)
            st.write(output_data)
            
            if st.button("Offshore"):
                month = st.text_input("Month")
                st.write(month)
                output_filename = f"BPCO_{month}.csv"
                towrite = BytesIO()
                pd.DataFrame(output_data).to_csv(towrite, index=False)
                towrite.seek(0)
                st.download_button(
                    label="Download Offshore results",
                    data=towrite,
                    file_name=output_filename,
                    mime="text/csv"
                )
            
            if st.button("Fund"):
                month = st.date_input("Month")
                fund_code = st.selectbox("Fund Number", ["II", "I"])
                output_filename = f"BPC{fund_code}_{month}.csv"
                towrite = BytesIO()
                pd.DataFrame(output_data).to_csv(towrite, index=False)
                towrite.seek(0)

                st.download_button(
                    label="Download Fund results",
                    data=towrite,
                    file_name=output_filename,
                    mime="text/csv"
                )
        else:
            st.write("Please upload an Excel file.")
    else:
        st.write("No file uploaded yet.")

if __name__ == "__main__":
    main()