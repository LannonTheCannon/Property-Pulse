import streamlit as st
import pandas as pd
from io import StringIO
import openai
import time
import time

from numpy.f2py.auxfuncs import isinteger

from database import Database

client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
assistant_id = 'asst_uIhuW3xlt1ewEN6avGZJQ25l'
thread_id = 'thread_07h06ai63JWKKcKkjuqKGyoA'

# initialize database
db = Database()

# Load Data from SQLite (Instead of CSV)
df = db.execute_query("SELECT * FROM properties")

def get_columns():
    print(df.columns)

def view_listings():
    print(df.head(5))

def df_names():
    # Play around with the dataframe
    new_df = df[['name', 'host_name']]

    # Get all the locations with a price that's less than a certain number
    play_df = df[df['price'] < 5]

    print(play_df)

def prepare_dataset_summary():
    buffer = StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()

    summary = f"""
    Dataset Summary:

    Number of rows: {len(df)}
    Number of columns: {len(df.columns)}

    Column descriptions:
    {info_string}

    Basic statistics:
    {df.describe().to_string()}

    Sample data (first 5 rows):
    {df.head().to_string()}
    """
    return (summary)

def update_assistant_with_dataset():

    dataset_summary = prepare_dataset_summary()

    try:
        client.beta.assistants.update(
            assistant_id=assistant_id,
            instructions=f"You are an AI assistant specializing in Real Estate data"
                         f"Use the following dataset information to provide insights and answer questions:\n\n"
                         f"{dataset_summary}"
        )
        #st.success("Assistant updated with dataset information.")
        print('Assistant updated with dataset information')

    except Exception as e:
        #st.error(f"Error updating assistant: {str(e)}")
        print(f'Error updating assistant {str(e)}')

def get_assistant_response(client, assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)

        # Retrieve the assistant's messages
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        # Return the latest assistant message
        return messages.data[0].content[0].text.value

    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."

def display_ai_chat(client, assistant_id, thread_id):
    print("\n💬 Chat with AI about the Dataset (Type 'exit' to quit)\n")

    messages = []  # Store chat history

    while True:
        # User Input
        prompt = input("You: ")

        if prompt.lower() == "exit":
            print("\n👋 Exiting chat. Have a great day!")
            break

        messages.append({"role": "user", "content": prompt})

        # Get AI Response
        full_response = get_assistant_response(client, assistant_id, thread_id, prompt)
        print(f"AI: {full_response}\n")

        messages.append({"role": "assistant", "content": full_response})

if __name__ == '__main__':

    againChoice = True

    while againChoice:
        menu = input('''Please enter a menu item: 
        
                1. Get Columns 
                2. View Listings Headings 
                3. Function Playground (Pandas) 
                4. Update Assistant with Data 
                5. Interface Chat
                6. Enter any other key to exit 
                
        ''')

        try:
            if menu == '1':
                get_columns()
            elif menu == '2':
                view_listings()
            elif menu == '3':
                df_names()
            elif menu == '4':
                update_assistant_with_dataset()
            elif menu == '5':
                display_ai_chat(client, assistant_id, thread_id)
            else:
                print('Exiting...')
                time.sleep(2)
                break

        except ValueError:
            pass

        againChoice = (input('Would you like to try again? (Y/N)') == 'Y')
