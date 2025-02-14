import streamlit as st
import pandas as pd
import altair as alt
import time
import openai
import os
import logging
import io
from src.agenda_1 import agenda
from src.integration_plan_3 import integration_plan
from src.implementation_timeline_4 import implementation_timeline
from src.costs_roi_5 import costs_and_roi
from src.next_steps_6 import next_steps
import pandas as pd
import sqlite3
from database import Database

# Set page config
st.set_page_config(
    page_title="AI-Powered Real Estate Chatbot",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #4e54c8, #8f94fb);
    }
    .Widget>label {
        color: #4e54c8;
        font-weight: bold;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4e54c8;
        border-radius: 5px;
    }
    .stProgress .st-bo {
        background-color: #4e54c8;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #4e54c8;
    }
</style>
""", unsafe_allow_html=True)

# DB Connection #############################################################################
db = Database()

# Setup #####################################################################################
# Load secret key
api_key = st.secrets['OPENAI_API_KEY']
client = openai.OpenAI(api_key=api_key)

logging.basicConfig(level=logging.INFO)
ASSISTANT_ID = 'asst_uIhuW3xlt1ewEN6avGZJQ25l'
THREAD_ID = 'thread_BofkryfRaWSseJ2BwkeFlD7J'

# Main Functions for Response Retrieval ######################################################
def wait_for_run_complete(thread_id, run_id):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed))
                logging.info(f'Run completed in {formatted_elapsed_time}')
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                return last_message.content[0].text.value
        except Exception as e:
            logging.error(f'An error occurred while retrieving the run: {e}')
            return 'Sorry, I encountered an error. Please try again.'
        time.sleep(1)

def check_active_runs(thread_id):
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    for run in runs.data:
        if run.status == "in_progress":
            return run.id
    return None

def fetch_response(user_input):
    try:
        active_run_id = check_active_runs(THREAD_ID)
        if active_run_id:
            wait_for_run_complete(THREAD_ID, active_run_id)

        sql_generation_prompt = f"""Given the following SQL table schema:

    CREATE TABLE properties (
        id INTEGER PRIMARY KEY,
        address TEXT,
        price INTEGER,
        bedrooms INTEGER,
        bathrooms INTEGER,
        description TEXT
    )

    Generate a SQL query to answer the following question:
    {user_input}

    Return only the SQL query, without any additional text or markdown formatting."""

        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role='user',
            content=sql_generation_prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )

        sql_query = wait_for_run_complete(THREAD_ID, run.id)
        sql_query = sql_query.strip('`').replace('sql\n', '')

        # Now using db.execute_query instead of the global function
        query_result = db.execute_query(sql_query)

        if query_result is not None and not query_result.empty:
            query_result_str = query_result.to_string(index=False)
        else:
            query_result_str = "No results found for the given query."

        interpretation_prompt = f"""SQL Query: {sql_query}

Query Result:
{query_result_str}

User Question: {user_input}

You are a real estate chatbot. Provide an accurate and helpful response based on the SQL query, its results, and the user's original question.
If the query didn't return any results, suggest the user ask about available properties or provide general information about the listings.
For questions not related to real estate, politely redirect the conversation to property topics.

Remember previous questions and context from this conversation when formulating your response."""

        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role='user',
            content=interpretation_prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )

        response = wait_for_run_complete(THREAD_ID, run.id)
        return response

    except openai.APIError as e:
        if "Can't add messages to thread" in str(e):
            logging.warning("Caught active run error, retrying...")
            time.sleep(2)
            return fetch_response(user_input)
        else:
            logging.error(f"OpenAI API error: {str(e)}")
            return "Sorry, I encountered an API error. Please try again later."
    except Exception as e:
        logging.error(f'Error in fetch_response: {str(e)}', exc_info=True)
        return "I apologize, but I'm having trouble processing that request. Is there anything specific about our real estate listings you'd like to know?"


# Main function
def main():
    st.sidebar.title("🏠 A+ Realty & Mortgage")
    sections = [
        "Home",
        "AI Chatbot Demo",
        "Integration Plan",
        "Implementation Timeline",
        #"Costs and ROI",
        "Next Steps"
    ]
    selected_section = st.sidebar.radio("Navigation", sections)

    if selected_section == "Home":
        agenda()
    elif selected_section == "AI Chatbot Demo":
        chatbot_demo()
    elif selected_section == "Integration Plan":
        integration_plan()
    elif selected_section == "Implementation Timeline":
        implementation_timeline()
    # elif selected_section == "Costs and ROI":
    #     costs_and_roi()
    elif selected_section == "Next Steps":
        next_steps()
##
def chatbot_demo():
    st.markdown('<p class="big-font">AI Chatbot Demo</p>', unsafe_allow_html=True)
    st.write("Experience the power of AI-driven real estate assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about our properties"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in fetch_response(prompt):
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
if __name__ == "__main__":
    main()
