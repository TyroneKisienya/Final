import streamlit as st
from Login_page import login_page
from Register_page import registration_page

# Main app logic
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

def show_login_page():
    st.session_state['page'] = 'login'

def show_registration_page():
    st.session_state['page'] = 'register'

if st.session_state['login_status']:
    st.write("Welcome to the app!")
    if st.button("Logout"):
        st.session_state['login_status'] = False
        st.session_state['page'] = 'login'
else:
    if st.session_state['page'] == 'login':
        login_page()
        if st.button("Go to Registration"):
            show_registration_page()
    elif st.session_state['page'] == 'register':
        registration_page()
        if st.button("Go to Login"):
            show_login_page()
