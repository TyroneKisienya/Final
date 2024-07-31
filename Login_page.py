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

def validate_user(conn, email, password):
    sql_query = "SELECT email FROM users WHERE email = %s AND password = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query, (email, password))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False

def login_page(change_page):
    st.title("Login Page")

    with st.form("login_form"):
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Login")

    if login_submitted:
        conn = create_connection()
        if conn is not None:
            if validate_user(conn, login_email, login_password):
                st.success("Login successful!")
                return login_email
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Failed to connect to database.")

    if st.button("Back to Home"):
        change_page("landing")
    
    return None

if __name__ == "__main__":
    login_page()