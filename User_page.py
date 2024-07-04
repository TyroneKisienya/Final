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

def get_user_details(conn, email):
    sql_query = "SELECT first_name, last_name, email FROM users WHERE email = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query, (email,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def user_page(email):
    st.title("User Page")

    conn = create_connection()
    if conn is not None:
        user_details = get_user_details(conn, email)
        if user_details:
            first_name, last_name, user_email = user_details
            st.write(f"Welcome, {first_name} {last_name}!")
            st.write(f"Email: {user_email}")
        else:
            st.error("User not found.")
    else:
        st.error("Failed to connect to database.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()