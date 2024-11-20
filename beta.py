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
    
if __name__ == "__main__":
    main()