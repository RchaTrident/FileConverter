import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import uuid
from utils import database, auth

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

def main():
    conn = get_snowflake_connection()