import streamlit as st
import mysql.connector
import requests

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

def search_drug(drug_name):
    base_url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.brand_name:{drug_name}",
        "limit": 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['meta']['results']['total'] > 0:
            drug_info = data['results'][0]
            return {
                "brand_name": drug_info['openfda'].get('brand_name', ['N/A'])[0],
                "generic_name": drug_info['openfda'].get('generic_name', ['N/A'])[0],
                "manufacturer": drug_info['openfda'].get('manufacturer_name', ['N/A'])[0],
                "purpose": drug_info.get('purpose', ['N/A'])[0],
                "warnings": drug_info.get('warnings', ['N/A'])[0]
            }
        else:
            return None
    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
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
            drug_name=st.columns(8)[-8].text_input("Search Medicine")
            if st.button("Search"):
                if drug_name:
                    with st.spinner("Searching..."):
                        drug_info = search_drug(drug_name)
                    if drug_info:
                        st.subheader(f"Information for {drug_info['brand_name']}")
                        st.write(f"Generic Name: {drug_info['generic_name']}")
                        st.write(f"Manufacturer: {drug_info['manufacturer']}")
                        st.write(f"Purpose: {drug_info['purpose']}")
                        st.write("Warnings:")
                        st.write(drug_info['warnings'])
                    else:
                        st.warning("No information found for this drug.")
                else:
                    st.warning("Please enter a drug name.")

            st.page_link("https://www.google.com/maps/search/?api=1&query=nearest+chemists+to+my+current+location", label="Find Chemists", icon="🌎")
            # Add more dashboard content here
        else:
            st.error("User not found.")
    else:
        st.error("Failed to connect to database.")

