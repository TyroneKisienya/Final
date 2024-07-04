import streamlit as st
import mysql.connector
import hashlib

# Function to check if a user exists and the password is correct
def login_user(national_id, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        c = conn.cursor(buffered=True)
        c.execute('SELECT * FROM users WHERE national_id = %s AND password = %s', (national_id, password))
        data = c.fetchone()
        conn.close()
        return data
    except mysql.connector.Error as e:
        st.error(f"Error logging in: {e}")
        return None

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Layout for the login page
def login_page():
    st.title("Login")
    with st.form(key='login_form'):
        national_id = st.text_input("National ID")
        password = st.text_input("Password", type='password')
        login_button = st.form_submit_button(label='Login')

        if login_button:
            hashed_password = hash_password(password)
            result = login_user(national_id, hashed_password)
            if result:
                st.success("Logged in successfully.")
                st.session_state['login_status'] = True
            else:
                st.warning("User does not exist or password is incorrect.")
