import streamlit as st
from landing_page import landing_page
from Login_page import login_page
from User_page import user_page
from Register_page import registration_page

def main():
    st.set_page_config(page_title="Safespace", page_icon="🏠")

    #st.set_page_config(page_title="Safespace", page_icon="🏠")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = None

    if "page" not in st.session_state:
        st.session_state.page = "landing"

    # Function to change pages
    def change_page(new_page):
        st.session_state.page = new_page
        st.experimental_rerun()

    # Sidebar navigation (only show for non-landing pages)
    if st.session_state.page != "landing":
        with st.sidebar:
            st.title("Navigation")
            if st.button("Home"):
                change_page("landing")
            if st.button("Login"):
                change_page("login")
            if st.button("Register"):
                change_page("register")

    # Main content
    if not st.session_state.logged_in:
        if st.session_state.page == "landing":
            landing_page(change_page)
        elif st.session_state.page == "register":
            registration_page(change_page)
        elif st.session_state.page == "login":
            email = login_page(change_page)
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.experimental_rerun()
    else:
        user_page(st.session_state.user_email, change_page)

if __name__ == "__main__":
    main()