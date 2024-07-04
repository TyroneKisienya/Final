import streamlit as st
from Login_page import login_page
from Register_page import registration_page, create_users_table

# Main app logic
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False

if st.session_state['login_status']:
    st.write("Welcome to the app!")
else:
    create_users_table()
    if st.button("Go to Registration"):
        registration_page()
    else:
        login_page()
