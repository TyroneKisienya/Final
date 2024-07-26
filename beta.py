import streamlit as st
from drug_recommender import recommend_drugs

def main():
    st.set_page_config(layout="wide")

    # Recommendation Section
    st.subheader("Drug Recommendation")
    user_input = st.text_area("Describe your condition or symptoms:")
    if st.button("Get Recommendations"):
        if user_input:
            recommendations = recommend_drugs(user_input)  # Get only top recommendation
            st.write("Recommended drugs based on your description:")
            for reason, drugs in recommendations:
                st.write(f"**Reason:** {reason}")
                st.write("**Recommended drugs:**")
                for drug in drugs[:5]:  # Limit to top 5 drugs
                    st.write(f"- {drug}")
                st.write("---")
        else:
            st.warning("Please enter a description of your condition.")
    
    # Page link to find chemists
    st.page_link("https://www.google.com/maps/search/?api=1&query=nearest+chemists+to+my+current+location", label="Find Chemists", icon="🌎")

if __name__ == "__main__":
    main()