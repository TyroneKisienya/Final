import streamlit as st
from drug_recommender import recommend_drugs

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