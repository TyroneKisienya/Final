import streamlit as st
import mysql.connector
import requests
from twilio.rest import Client
from drug_recommender import recommend_drugs

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
    
def get_user_location():
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if latitude and longitude:
            return latitude, longitude
        else:
            return None
    except:
        return None

def get_emergency_contact(conn, email):
    sql_query = "SELECT emergency_name, emergency_phone FROM users WHERE email = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query, (email,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

# Twillio credentials

def send_emergency_whatsapp(to_phone, user_name, latitude, longitude):
    account_sid =''
    auth_token = ''
    from_phone = ''  

    client = Client(account_sid, auth_token)

    try:
        # Send text message
        text_message = f"Emergency Alert! {user_name} needs assistance."
        client.messages.create(
            body=text_message,
            from_=from_phone,
            to=f"whatsapp:{to_phone}"
        )

        # Send location message
        location_message = client.messages.create(
            from_=from_phone,
            to=f"whatsapp:{to_phone}",
            body=f"{user_name}'s Location",
            persistent_action=[f"geo:{latitude},{longitude}|{user_name}'s Location"]
        )

        return True
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return False

def user_page(email):
    st.set_page_config(layout="wide")

    # CSS for positioning
    
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

            # Main Dashboard content
            st.markdown(f"""
            <div class="user">
                <p><strong>Welcome {first_name}</strong></p>
            </div>
            """, unsafe_allow_html=True)

             # recommendation Section
            st.subheader("Drug Recommendation")
            user_input = st.text_area("Describe your condition or symptoms:")
            if st.button("Get Recommendations"):
                if user_input:
                    recommendations = recommend_drugs(user_input)
                    st.write("Recommended drugs based on your description:")
                    for reason, drugs in recommendations:
                        st.write(f"**Reason:** {reason}")
                        st.write(f"**Recommended drugs:**")
                        for drug in drugs[:5]:  # Limit to top 5 drugs
                            st.write(f"- {drug}")
                        st.write("---")
                else:
                    st.warning("Please enter a description of your condition.")
            
            if st.button("Send Emergency WhatsApp"):
                conn = create_connection()
                if conn is not None:
                    emergency_contact = get_emergency_contact(conn, email)
                    if emergency_contact:
                        emergency_name, emergency_whatsapp = emergency_contact
                        location = get_user_location()
                        user_details = get_user_details(conn, email)
                        user_name = f"{user_details[0]} {user_details[1]}"

                        if location:
                            latitude, longitude = location
                            if send_emergency_whatsapp(emergency_whatsapp, user_name, latitude, longitude):
                                st.success("Emergency WhatsApp message with location sent successfully!")
                            else:
                                st.error("Failed to send emergency WhatsApp message.")
                        else:
                            st.error("Unable to retrieve location. Emergency message sent without location.")
                    else:
                        st.error("Emergency contact information not found.")
                else:
                    st.error("Failed to connect to database.")

            st.page_link("https://www.google.com/maps/search/?api=1&query=nearest+chemists+to+my+current+location", label="Find Chemists", icon="🌎")
        else:
            st.error("User not found.")
    else:
        st.error("Failed to connect to database.")

