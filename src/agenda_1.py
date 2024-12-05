import streamlit as st


def agenda():
    # Hero Section
    st.markdown('<h1 style="text-align: center;">Property Pulse</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Your AI Real Estate Assistant</h3>', unsafe_allow_html=True)

    # Main image and intro
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Ask me anything about our properties! 👋

        I can help you:
        - Find homes within your budget 💰
        - Compare different properties 🏠
        - Learn about neighborhoods 🌳
        - Get property details instantly ⚡

        Just type your question in the chat below!
        """)
    with col2:
        st.image('./images/ai_real_estate.jpg')

    # Quick Start Guide
    st.markdown("### 💡 Try asking questions like:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Finding Properties")
        st.write("💬 'What homes are available under $400,000?'")
        st.write("💬 'Show me houses with 3 bedrooms'")
        st.write("💬 'Which properties have pools?'")

    with col2:
        st.markdown("#### Comparing Options")
        st.write("💬 'What's the price range for 4-bedroom homes?'")
        st.write("💬 'Tell me about downtown properties'")
        st.write("💬 'Compare houses with large yards'")

    # Features with simple icons
    st.markdown("### ✨ What Makes Property Pulse Special")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🎯 For Home Buyers
        - Quick answers about any property
        - Easy price comparisons
        - Neighborhood information
        - Available 24/7
        """)

    with col2:
        st.markdown("""
        #### 🏆 For Real Estate Agents
        - Automatic property matching
        - Quick client responses
        - Easy listing management
        - More time for what matters
        """)

    # How it Works
    st.markdown("### 🤔 How It Works")
    st.markdown("""
    1. **Ask a Question** - Type anything about properties
    2. **Get Instant Answers** - AI finds the perfect matches
    3. **Explore Details** - Learn more about each property
    4. **Stay Informed** - Get updates on new listings
    """)

    # Success Metrics in a friendly way
    st.markdown("### 📈 Why People Love Property Pulse")

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Super Fast", "2 seconds", "average response time")

    with metric_col2:
        st.metric("Super Smart", "94%", "accuracy")

    with metric_col3:
        st.metric("Super Helpful", "100+", "daily chats")

    # Get Started Section
    st.info("""
    ### 👋 Ready to Start?
    Click **"AI Chatbot Demo"** in the sidebar to start chatting!

    Need help? Just ask "How can you help me?" in the chat.
    """)

    # Optional: Fun Facts
    with st.expander("🎈 Fun Facts About Property Pulse"):
        st.markdown("""
        - Can search through 1000+ properties in seconds
        - Speaks in plain English (no real estate jargon!)
        - Updates property info in real-time
        - Remembers your preferences for better recommendations
        """)