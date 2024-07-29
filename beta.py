import streamlit as st
from drug_recommender import recommend_drugs
from twilio.rest import Client
import re

def is_valid_phone_number(number):
    pattern = r'^\+254\d{9}$'
    return re.match(pattern, number) is not None

def send_sms(to_phone, message):
    account_sid = st.secrets["twilio_account_sid"]
    auth_token = st.secrets["twilio_auth_token"]
    from_phone = st.secrets["twilio_phone_number"]

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        return True
    except Exception as e:
        st.error(f"Error sending SMS: {e}")
        return False

def main():
    st.set_page_config(layout="wide")

    # Phone number input
    phone_number = st.text_input("Enter your phone number (format: +254XXXXXXXXX):")
    
    if phone_number and not is_valid_phone_number(phone_number):
        st.warning("Please enter a valid phone number in the format +254XXXXXXXXX")

    # Recommendation Section
    st.subheader("Drug Recommendation")
    user_input = st.text_area("Describe your condition or symptoms:")
    if st.button("Get Recommendations"):
        if user_input:
            recommendations = recommend_drugs(user_input)
            st.write("Recommended drugs based on your description:")
            recommendation_text = ""
            for i, (reason, drugs) in enumerate(recommendations[:5]):  # Limit to top 5 recommendations
                st.write(f"**Reason:** {reason}")
                st.write("**Recommended drugs:**")
                recommendation_text += f"Reason: {reason}\nRecommended drugs:\n"
                for drug in drugs[:5]:  # Limit to top 5 drugs
                    st.write(f"- {drug}")
                    recommendation_text += f"- {drug}\n"
                st.write("---")
                recommendation_text += "---\n"
                if i == 1:  # Break after 2 recommendations
                    break

            # Store recommendations in session state
            st.session_state.recommendation_text = recommendation_text
        else:
            st.warning("Please enter a description of your condition.")
    
    # Page link to find chemists
    chemist_link = "https://www.google.com/maps/search/?api=1&query=nearest+chemists+to+my+current+location"
    st.page_link(chemist_link, label="Find Chemists", icon="🌎")

    # Button to send SMS
    if st.button("Send Recommendations via SMS"):
        if phone_number and is_valid_phone_number(phone_number):
            if 'recommendation_text' in st.session_state:
                message = f"{st.session_state.recommendation_text}\nFind nearest chemists: {chemist_link}"
                if send_sms(phone_number, message):
                    st.success("Recommendations sent to your phone!")
                else:
                    st.error("Failed to send SMS. Please try again.")
            else:
                st.warning("Please get recommendations first before sending SMS.")
        else:
            st.warning("Please enter a valid phone number to receive recommendations.")

if __name__ == "__main__":
    main()