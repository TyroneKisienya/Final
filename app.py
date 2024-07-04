import streamlit as st
from Login_page import login_page
from User_page import user_page
from Register_page import registration_page

def main():
    query_params = st.query_params
    email = query_params.get("email", [None])[0]

    if email:
        user_page(email)
    else:
        login_page()

if __name__ == "__main__":
    main()
