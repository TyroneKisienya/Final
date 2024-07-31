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
    st.markdown("---")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    # Safespace
    Safespace is tailored for you. You have any verified medical symptoms or a reason or even a medical practitioner's recommendation,
        register your details and feed the model with the said information and get the best suggested medical drugs to use for treatment.
                Recommendations should be treated as suggestions and not as professional medical advice.
    """)

    st.markdown("### Get Help")
    st.markdown("User Manual'https://github.com/TyroneKisienya/Final/blob/main/Project%20Documentation%204.pdf'")

    st.markdown("### Report a Bug")
    st.markdown("Contact Me 'tyronekisienya01@gmail.com'")