# Start with what you know
#
# Simple OpenAI Assistant API
#
###########################################################################################################

# Importing the main libraries
import streamlit as st
import openai
from dotenv import load_dotenv
import os
import logging
import time

# Load environment variables
load_dotenv()

# Setup OpenAI Client
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    st.error('OpenAI API key was not found. Please check your .env file.')
    st.stop()

# Setting up the OpenAI Client
client = openai.OpenAI(api_key=api_key)

# Set up logging
logging.basicConfig(level= logging.INFO)

# CONSTANTS
ASSISTANT_ID = 'asst_kGpo0qVcgHp4R5kItDuUNMZB'
THREAD_ID = 'thread_EiCMg9fI3uwF4cWUgWmM82ra'

# perform thread
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
            logging.error(f'An error occured while retrieving the run: {e}')
            return 'Sorry, i encountered an error. Please try again.'
        time.sleep(1)

def check_active_runs(thread_id):
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    for run in runs.data:
        if run.status == "in_progress":
            return run.id
    return None

def fetch_response(user_input):
    try:
        # Check for active runs
        active_run_id = check_active_runs(THREAD_ID)
        if active_run_id:
            # Wait for the active run to complete
            wait_for_run_complete(THREAD_ID, active_run_id)
        
        # Create a message in the thread
        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role='user',
            content=f'Please provide very brief responses, no more than 2-3 sentences or 50 words. {user_input}'
        )

        # Create a run with the assistant
        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )
        return wait_for_run_complete(THREAD_ID, run.id)

    except openai.APIError as e:
        if "Can't add messages to thread" in str(e):
            logging.warning("Caught active run error, retrying...")
            time.sleep(2)  # Wait a bit before retrying
            return fetch_response(user_input)  # Retry the request
        else:
            logging.error(f"OpenAI API error: {str(e)}")
            return "Sorry, I encountered an API error. Please try again later."
    except Exception as e:
        logging.error(f'Error in fetch_response: {str(e)}', exc_info=True)
        return f"Sorry, I encountered an error: {str(e)}"

# Streamlit UI
st.title('A+ Realty and Mortgage Chatbot')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('What would you like to know about A+ mortgages?'):
    # Display user message in chat message container
    st.chat_message('user').markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = fetch_response(prompt)

    # Display assistant response in chat message container
    with st.chat_message('assistant'):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({'role': 'assistant', 'content': response})


        
                



                
