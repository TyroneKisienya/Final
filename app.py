import streamlit as st
from Login_page import login_page
from User_page import user_page
from Register_page import registration_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Register"])

    if page == "Login":
        email = login_page()
        if email:
            user_page(email)
    elif page == "Register":
        registration_page()

if __name__ == "__main__":
    main()