import streamlit as st
from Login_page import login_page
from User_page import user_page
from Register_page import registration_page

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = None

    if not st.session_state.logged_in:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Login", "Register"])

        if page == "Login":
            email = login_page()
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
        elif page == "Register":
            registration_page()
    else:
        user_page(st.session_state.user_email)

if __name__ == "__main__":
    main()