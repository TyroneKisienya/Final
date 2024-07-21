import streamlit as st
import mysql.connector

def create_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fushiguro@11",
            database="users"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
    except mysql.connector.Error as e:
        print(e)
    return conn

def create_user_table(conn):
    sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            emergency_name VARCHAR(255),
            emergency_phone VARCHAR(20),
            emergency_email VARCHAR(255)
        )
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_users_table)
        print("User table created")
    except mysql.connector.Error as e:
        print(e)

def insert_user(conn, user):
    sql_insert_user = """
        INSERT INTO users (first_name, last_name, phone_number, email, password, emergency_name, emergency_phone, emergency_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_insert_user, user)
        conn.commit()
        print("User inserted")
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return -1

def registration_page():
    st.title("User Registration")

    conn = create_connection()
    if conn is not None:
        create_user_table(conn)
    else:
        st.error("Failed to connect to database.")

    with st.form("registration_form"):
        st.write("Please fill out the registration form:")
        reg_first_name = st.text_input("First Name")
        reg_last_name = st.text_input("Last Name")
        reg_phone_number = st.text_input("Phone Number")
        reg_email = st.text_input("Email")
        reg_password = st.text_input("Password", type="password")
        reg_emergency_name = st.text_input("Emergency Contact Name")
        reg_emergency_phone = st.text_input("Emergency Contact Phone Number")
        reg_emergency_email = st.text_input("Emergency Contact Email")
        reg_submitted = st.form_submit_button("Register")

    if reg_submitted:
        if reg_first_name and reg_last_name and reg_phone_number and reg_email and reg_password and reg_emergency_name and reg_emergency_phone and reg_emergency_email :
            reg_user = (reg_first_name, reg_last_name, reg_phone_number, reg_email, reg_password, reg_emergency_name, reg_emergency_phone, reg_emergency_email )
            if conn.is_connected():
                user_id = insert_user(conn, reg_user)
                if user_id != -1:
                    st.success("Registration successful! User ID: {}".format(user_id))
                    st.info("Please go to the Login page to sign in.")
                else:
                    st.error("Failed to register user.")
            else:
                st.error("Lost connection to the database.")
        else:
            st.warning("Please fill out all fields.")

if __name__ == "__main__":
    registration_page()