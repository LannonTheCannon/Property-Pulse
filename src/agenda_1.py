# agenda_1.py
import streamlit as st

def agenda():
    st.markdown('<p class="big-font">Welcome to the AI-Powered Real Estate Chatbot Demo</p>', unsafe_allow_html=True)
    st.write("Empowering A+ Realty & Mortgage with cutting-edge AI technology")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        Our AI-powered chatbot solution offers:
        - 🎯 Highly accurate responses to property queries
        - 🔄 Seamless handling of frequently changing listing data
        - 🧠 Ability to answer complex, context-dependent questions
        - 🚀 24/7 availability to engage with potential clients
        """)
    with col2:
        st.image("https://cdn.discordapp.com/attachments/1109716744978837587/1270829761387827332/ai_real_estate.jpg?ex=66b51ff1&is=66b3ce71&hm=3a963b2d2a0819334241f06c2f871a1467b102ac033ebe3eca94798aa315ba54&", width=300)

    st.info("Navigate through the sections using the sidebar to explore the full capabilities of my solution.")
    st.divider()
    st.markdown('<p class="big-font">Today\'s Meeting Agenda</p>', unsafe_allow_html=True)
    st.markdown("""
    1. Introduction (3 minutes)
    2. Client Needs Recap (5 minutes)
    3. Proposed Solution: Hybrid AI-Database System (10 minutes)
    4. Integration Plan (7 minutes)
    5. Implementation Timeline (5 minutes)
    6. Costs and ROI (10 minutes)
    7. Key Benefits for A+ Realty & Mortgage (5 minutes)
    8. Case Study or Success Story (3 minutes)
    9. Next Steps and Commitment (7 minutes)
    10. Q&A Session (10 minutes)
    11. Closing Remarks (5 minutes)
    """)

    with st.expander("View Detailed Agenda"):
        st.markdown("""
        1. **Introduction (3 minutes)**
           - Brief overview of the meeting objectives
        2. **Client Needs Recap (5 minutes)**
           - Highly accurate chatbot responses
           - Website and robots integration
           - Flexibility for frequent listing data updates
        3. **Proposed Solution: Hybrid AI-Database System (10 minutes)**
           - Overview of system components:
             - Real-time database for listings
             - Natural Language to SQL (NL2SQL) system
             - AI Language Model
           - Explanation of how this ensures high accuracy and flexibility
           - Demo of initial prototype (if available)
        4. **Integration Plan (7 minutes)**
           - Process for integrating with client's website
           - Approach for robot integration
           - Data update mechanisms for frequent listing changes
        5. **Implementation Timeline (5 minutes)**
           - 5-month timeline overview
           - Breakdown of 4 project phases
        6. **Costs and ROI (10 minutes)**
           - Total project cost: $26,000
           - Payment structure aligned with 4 phases
           - Projected ROI:
             - Estimated increase in lead generation
             - Potential time saved for sales team
             - Improved customer satisfaction metrics
        7. **Key Benefits for A+ Realty & Mortgage (5 minutes)**
           - 24/7 availability with highly accurate responses
           - Improved customer engagement
           - Competitive edge in the real estate market
           - Scalability for growing inventory
        8. **Case Study or Success Story (3 minutes)**
           - Brief example of a similar implementation
        9. **Next Steps and Commitment (7 minutes)**
           - Proposal for immediate project initiation
           - Discussion of first phase deliverables
           - Request for $26,000 commitment over 5 months
        10. **Q&A Session (10 minutes)**
            - Address any concerns or questions
        11. **Closing Remarks (5 minutes)**
            - Recap of key benefits and timeline
            - Express enthusiasm for the partnership
            - Confirm next steps and commitment
        """)
