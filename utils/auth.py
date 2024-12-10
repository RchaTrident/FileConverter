import streamlit as st
import hashlib
import requests
import json
import streamlit.components.v1 as components


user_roles = {
    "FINICITYTTUS": {
        "tables": ["ALL"],
        "customers": "ALL"
    },
    "TRIDENT_LORENZ": {
        "tables": ["TESTINGAI.TESTINGAISCHEMA.TIOGA"],
        "customers": ["Lee's Customer"]
    }
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    stored_username = st.secrets.get(f"{username.upper()}_USERNAME")
    stored_password = st.secrets.get(f"{username.upper()}_PASSWORD")
    if not stored_username or not stored_password:
        st.error("Authentication credentials not configured")
        return False
    
    if username in user_roles and hash_password(password) == hash_password(stored_password):
        st.session_state['user_role'] = username
        return True
    else:
        return False

def login_page():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Custom HTML to trigger input events
    components.html("""
        <script>
            const usernameInput = document.querySelector('input[aria-label="Username"]');
            const passwordInput = document.querySelector('input[aria-label="Password"]');
            
            usernameInput.addEventListener('input', () => {
                usernameInput.dispatchEvent(new Event('change', { bubbles: true }));
            });
            
            passwordInput.addEventListener('input', () => {
                passwordInput.dispatchEvent(new Event('change', { bubbles: true }));
            });
        </script>
    """, height=0)
    
    if st.button("Login"):
        print(username, password)
        if not username or not password:
            st.error("Please enter both username and password")
        elif authenticate(username, password):
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state['logged_in'] = False
    st.rerun() 

def display_content():
    user_role = st.session_state.get('user_role')
    if user_role:
        st.write(f"Logged in as: {user_role}")
        if user_role == "admin":
            st.write("Admin content here...")
        elif user_role == "lee":
            st.write("Lee's content here...")
            st.write("Access to tables:", user_roles[user_role]["tables"])
            st.write("Access to customers:", user_roles[user_role]["customers"])
    else:
        st.write("No role assigned.")

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        if st.button("Logout"):
            logout()
        display_content()
    else:
        login_page()