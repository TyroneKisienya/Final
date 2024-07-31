import streamlit as st

def landing_page(change_page):
    st.markdown("<h1 style='text-align: center; font-size: 4em;'>Safespace</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        if st.button("Register", key="register_button", use_container_width=True):
            change_page("register")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Login", key="login_button", use_container_width=True):
            change_page("login")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Move to Beta App", key="beta_button", use_container_width=True):
            st.markdown("[Go to Beta App](https://safespace.streamlit.app)")

    st.markdown(
        """
        <style>
        .stButton>button {
            width: 100%;
            height: 3em;
            font-size: 1.5em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )