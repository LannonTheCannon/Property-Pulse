# Integration Plan
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def integration_plan():
    st.markdown('<p class="big-font">Integration Plan</p>', unsafe_allow_html=True)
    st.write("Seamless integration with your existing systems")

    # Integration architecture diagram
    st.subheader("Integration Architecture")
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = ["Website", "Chatbot", "Database", "MLS API", "3rd Party APIs", "Users"],
          color = "blue"
        ),
        link = dict(
          source = [0, 1, 1, 1, 2, 3, 4],
          target = [1, 2, 3, 4, 1, 1, 1],
          value = [8, 4, 2, 2, 4, 2, 2]
      ))])

    fig.update_layout(title_text="Data Flow in Integrated System", font_size=10)
    st.plotly_chart(fig)
    
    st.subheader("How Our Integrated System Works")

    # Custom CSS for cards
    st.markdown("""
    <style>
    .card {
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .icon {
        font-size: 24px;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # System components
    st.markdown("### System Components")
    col1, col2 = st.columns(2)
    
    components = [
        ("1. 🌐 Website", "Starting point for user interactions"),
        ("2. 🤖 Chatbot", "Central hub of the system"),
        ("3. 💾 Database", "Contains all property listings and information"),
        ("4. 🔗 MLS API", "Access to broader range of listings and market data"),
        ("5. 🧰 3rd Party APIs", "Additional services like mortgage calculators"),
        ("6. 👥 Users", "End-users interacting with the system")
    ]
    
    for i, (icon, desc) in enumerate(components):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="card">
            <span class="icon">{icon}</span> <strong>{desc.split(':')[0]}</strong><br>
            {desc.split(':')[1] if ':' in desc else desc}
            </div>
            """, unsafe_allow_html=True)

    # Data flow
    st.markdown("### Data Flow")
    data_flow = [
        "1. 🌐➡️🤖 Website to Chatbot: User queries are passed to the chatbot",
        "2. 🤖➡️💾 Chatbot to Database: Chatbot retrieves property information",
        "3. 💾➡️🤖 Database to Chatbot: Information is sent back to the chatbot",
        "4. 🤖➡️🔗 Chatbot to MLS API: Chatbot queries for additional listings",
        "5. 🔗➡️🤖 MLS API to Chatbot: Additional property data is returned",
        "6. 🤖➡️🧰 Chatbot to 3rd Party APIs: Chatbot requests supplementary info",
        "7. 🧰➡️🤖 3rd Party APIs to Chatbot: Supplementary data is returned",
        "8. 🤖➡️👥 Chatbot to Users: Compiled information is presented to users"
    ]

    for flow in data_flow:
        st.markdown(f"<div class='card'>{flow}</div>", unsafe_allow_html=True)

    st.success("This integrated system acts like a super-knowledgeable real estate agent, available 24/7 to provide your customers with the best service possible!")

    st.info("This system ensures that your customers always get accurate, up-to-date information, enhancing their experience and potentially boosting your sales!")

    # Key benefits
    st.subheader("Key Benefits of Our Integration Approach")

    benefits = {
        'Seamless User Experience': 'Ensures smooth interaction between users and the AI chatbot across all platforms.',
        'Real-time Data Accuracy': 'Provides up-to-date information by syncing with your database and MLS in real-time.',
        'Scalability': 'Easily adapts to growing inventory and increasing user base without performance loss.',
        'Enhanced Security': 'Implements robust data protection measures to safeguard sensitive information.',
        'Improved Customer Engagement': 'Offers 24/7 availability, quick responses, and personalized interactions.',
        'Operational Efficiency': 'Automates routine inquiries, freeing up your team for high-value tasks.'
    }

    fig = go.Figure(go.Table(
        header=dict(values=['Benefit', 'Description'],
                    fill_color='#4e54c8',
                    align='left',
                    font=dict(color='white', size=16)),
        cells=dict(values=[list(benefits.keys()), list(benefits.values())],
                   fill_color='#f3f3f3',
                   align='left',
                   font=dict(color='#333', size=14))
    ))

    fig.update_layout(
        title='Integration Benefits Overview',
        height=400,
        margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("These benefits combine to create a powerful, efficient, and user-friendly real estate platform that sets your business apart from the competition.")

