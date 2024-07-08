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
    st.set_page_config(layout="wide")
    # Custom CSS for positioning
    st.markdown("""
    <style>
    .user-info {
        position: fixed;
        top: 60px;
        right: 20px;
        z-index: 1000;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

    conn = create_connection()
    if conn is not None:
        user_details = get_user_details(conn, email)
        if user_details:
            first_name, last_name, user_email = user_details
            
            # User info at top right
            st.markdown(f"""
            <div class="user-info">
                <p><strong>{first_name} {last_name}</strong></p>
                <p>{user_email}</p>
            </div>
            """, unsafe_allow_html=True)

            # Logout button
            with st.container():
                st.markdown('<div class="logout-button">', unsafe_allow_html=True)
                if st.columns(13)[12].button("Logout"):
                    st.session_state.logged_in = False
                    st.session_state.user_email = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # Main content
            st.markdown(f"""
            <div class="user">
                <p><strong>Welcome {first_name}</strong></p>
            </div>
            """, unsafe_allow_html=True)

            st.page_link("https://www.google.com/maps/search/?api=1&query=nearest+chemists+to+my+current+location", label="Find Chemists", icon="🌎")
            # Add more dashboard content here
        else:
            st.error("User not found.")
    else:
        st.error("Failed to connect to database.")

