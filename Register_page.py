import streamlit as st
import mysql.connector
import hashlib

# Function to create users table if it doesn't exist
def create_users_table():
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(first_name TEXT, last_name TEXT, national_id TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

# Function to add a new user to the database
def add_user(first_name, last_name, national_id, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fushiguro@11",
        database="users"
    )
    c = conn.cursor()
    c.execute('INSERT INTO users (first_name, last_name, national_id, password) VALUES (%s, %s, %s, %s)', (first_name, last_name, national_id, password))
    conn.commit()
    conn.close()

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Function to check if all fields are filled
def check_fields(first_name, last_name, national_id, password, confirm_password):
    return all([first_name, last_name, national_id, password, confirm_password])

# Layout for the registration page
def registration_page():
    st.title("Registration")
    with st.form(key='register_form'):
        cols = st.columns(2)
        first_name = cols[0].text_input("First Name")
        last_name = cols[1].text_input("Last Name")
        national_id = st.text_input("National ID")
        cols = st.columns(2)
        password = cols[0].text_input("Password", type='password')
        confirm_password = cols[1].text_input("Confirm Password", type='password')
        submit_button = st.form_submit_button(label='Register')

        if submit_button:
            if check_fields(first_name, last_name, national_id, password, confirm_password):
                if password == confirm_password:
                    hashed_password = hash_password(password)
                    add_user(first_name, last_name, national_id, hashed_password)
                    st.success("You have successfully registered.")
                    st.balloons()
                else:
                    st.warning("Passwords do not match.")
            else:
                st.warning("All fields must be filled.")
