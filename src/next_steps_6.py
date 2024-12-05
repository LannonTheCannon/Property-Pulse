import streamlit as st
import plotly.express as px
from datetime import datetime

def next_steps():
    st.markdown('<p class="big-font">Your Journey to AI-Powered Real Estate Excellence</p>', unsafe_allow_html=True)
    st.write("Let's embark on this transformative journey together")

    # Timeline data
    timeline_data = [
        dict(Task="Test Integration", Start='2024-08-07', Finish='2024-08-28', Resource='Stage 1'),
        dict(Task="Database Connection", Start='2024-08-21', Finish='2024-09-11', Resource='Stage 1'),
        dict(Task="API Integration", Start='2024-09-04', Finish='2024-10-16', Resource='Stage 2'),
        dict(Task="Testing and QA", Start='2024-10-02', Finish='2024-11-13', Resource='Stage 3'),
        dict(Task="Final Deployment", Start='2024-11-06', Finish='2024-11-27', Resource='Stage 4'),
    ]

    # Convert string dates to datetime
    for item in timeline_data:
        item['Start'] = datetime.strptime(item['Start'], '%Y-%m-%d')
        item['Finish'] = datetime.strptime(item['Finish'], '%Y-%m-%d')

    # Create timeline visualization
    fig = px.timeline(timeline_data, x_start="Start", x_end="Finish", y="Task", color="Resource")
    fig.update_layout(
        title='Project Integration Timeline',
        xaxis_title='Date',
        yaxis_title='Integration Phase',
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed next steps
    st.subheader("Detailed Integration Steps")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 1. Test Integration (Aug 7 - Aug 28, 2024)
        - Set up initial test environment
        - Conduct preliminary integration tests
        - Identify potential challenges and solutions

        ### 2. Database Connection (Aug 21 - Sep 11, 2024)
        - Establish secure connection to your property database
        - Implement data synchronization protocols
        - Ensure data integrity and privacy compliance
        """)

    with col2:
        st.markdown("""
        ### 3. API Integration (Sep 4 - Oct 16, 2024)
        - Integrate with MLS API
        - Connect to relevant third-party services
        - Implement data consistency checks

        ### 4. Testing and QA (Oct 2 - Nov 13, 2024)
        - Conduct comprehensive system testing
        - Perform user acceptance testing
        - Address and resolve any identified issues

        ### 5. Final Deployment (Nov 6 - Nov 27, 2024)
        - Prepare for go-live
        - Conduct staff training
        - Execute deployment plan
        - Initiate post-launch monitoring
        """)

    # What to expect
    st.subheader("What to Expect During the Integration Process")
    st.markdown("""
    - Regular project status updates (bi-weekly)
    - Demonstration sessions of work-in-progress features
    - Opportunities for feedback and system refinement
    - Dedicated support team throughout the integration
    - Comprehensive documentation and training materials
    - Minimal disruption to your current operations
    """)

    # Call to action
    st.subheader("Ready to Revolutionize Your Real Estate Operations?")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Initiate Your AI Integration Now", key="start_integration"):
            st.success("Excellent decision! We're excited to begin this integration process with you.")
            st.balloons()
            st.markdown("""
            ### Thank you for choosing InStack AI Solutions as your AI integration partner!
            """)
