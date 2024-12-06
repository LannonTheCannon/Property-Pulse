# real_estate_chatbot_NL2SQL.py
#
# a simple web interface where users can ask questions about the properties. The chatbot will interpret these questions,
# conert them to SQL queries, execute them, and display the results
#
#=======================================================================================================================

import streamlit as st
import sqlite3
import pandas as pd
import re

# Set up the database
conn = sqlite3.connect('../../../Desktop/Property Pulse/A_Plus_Mortgage_Stuff/real_estate.db')
cursor = conn.cursor()

# Create a properties table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    address TEXT,
    price INTEGER,
    bedrooms INTEGER,
    bathrooms INTEGER,
    description TEXT
)
''')

# Insert sample data if the table is empty
cursor.execute("SELECT COUNT(*) FROM properties")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ('123 Main St', 300000, 3, 2, 'Beautiful house with garden'),
        ('456 Oak Ave', 450000, 4, 3, 'Spacious family home'),
        ('789 Pine Rd', 275000, 2, 1, 'Cozy starter home'),
        ('101 Elm St', 350000, 3, 2, 'Modern condo in city center'),
        ('202 Maple Dr', 500000, 5, 4, 'Luxury villa with pool')
    ]
    cursor.executemany('INSERT INTO properties (address, price, bedrooms, bathrooms, description) VALUES (?, ?, ?, ?, ?)', sample_data)
    conn.commit()

def nl_to_sql(question):
    question = question.lower()
    
    if 'cheapest' in question or 'lowest price' in question:
        return "SELECT * FROM properties ORDER BY price ASC LIMIT 1"
    elif 'most expensive' in question or 'highest price' in question:
        return "SELECT * FROM properties ORDER BY price DESC LIMIT 1"
    elif 'average price' in question:
        return "SELECT AVG(price) FROM properties"
    elif 'how many' in question and 'bedrooms' in question:
        return "SELECT address, bedrooms FROM properties"
    elif 'all properties' in question:
        return "SELECT * FROM properties"
    else:
        return "SELECT * FROM properties"

def execute_query(sql):
    return pd.read_sql_query(sql, conn)

def format_result(df, question):
    if 'average price' in question.lower():
        return f"The average price of properties is ${df.iloc[0, 0]:,.2f}"
    elif len(df) == 1:
        prop = df.iloc[0]
        return f"Property at {prop['address']} is ${prop['price']:,} with {prop['bedrooms']} bedrooms and {prop['bathrooms']} bathrooms"
    else:
        return df

def chatbot_response(question):
    sql = nl_to_sql(question)
    result_df = execute_query(sql)
    return format_result(result_df, question)

# Streamlit UI
st.title('Real Estate Chatbot')

user_question = st.text_input("Ask a question about our properties:")

if user_question:
    response = chatbot_response(user_question)
    
    if isinstance(response, str):
        st.write(response)
    else:
        st.dataframe(response)

# Close the database connection when the app is done
conn.close()
