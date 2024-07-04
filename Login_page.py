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

def login_user(conn, email, password):
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
        data = cursor.fetchone()
        if data and password == data[0]:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        print(e)
        return False

def login_page():
    st.title("Login")

    conn = create_connection()
    if conn is None:
        st.error("Failed to connect to database.")
        return

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Login")

    if login_submitted:
        if login_user(conn, email, password):
            st.success("Logged in successfully.")
            st.session_state['login_status'] = True
        else:
            st.warning("User does not exist or password is incorrect.")
