import streamlit as st
import openai
from dotenv import load_dotenv
import os
import logging
import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import io

# Load environment variables
load_dotenv()

# Setup OpenAI Client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error('OpenAI API key was not found. Please check your .env file.')
    st.stop()

client = openai.OpenAI(api_key=api_key)

# Set up logging
logging.basicConfig(level=logging.INFO)

# CONSTANTS
ASSISTANT_ID = 'asst_kGpo0qVcgHp4R5kItDuUNMZB'
THREAD_ID = 'thread_EiCMg9fI3uwF4cWUgWmM82ra'

# Load property data
data = """
address|price|bedrooms|bathrooms|description
123 Main St|300000|3|2|Beautiful house with garden, close to schools
456 Oak Ave|450000|4|3|Spacious family home, recently renovated kitchen
789 Pine Rd|275000|2|1|Cozy starter home, great for first-time buyers
321 Elm St|500000|5|4|Luxurious estate with pool and guest house
654 Maple Dr|325000|3|2|Charming bungalow, perfect for small families
987 Birch Ln|600000|4|3|Modern home with open floor plan and large yard
246 Cedar Ct|280000|2|1|Affordable townhouse, low maintenance
135 Willow St|350000|3|2|Classic colonial, well-maintained with upgrades
753 Aspen Blvd|410000|4|3|Contemporary design, near downtown amenities
159 Redwood Rd|475000|4|3|Elegant home in a desirable neighborhood
432 Birchwood Pl|320000|3|2|Renovated historic home, charming neighborhood
876 Cherry St|450000|4|3|Spacious suburban house, excellent school district
111 Pineapple Ln|330000|3|2|Eco-friendly home with solar panels
222 Orange Dr|420000|4|3|Lakefront property with stunning views
333 Lemon St|380000|3|2|Mountain cabin, secluded and private
444 Lime Blvd|360000|3|2|Urban loft, close to public transport
555 Mango Ct|440000|4|3|Beach house with private access
666 Grapefruit Rd|310000|2|1|Country home with acres of land
777 Apple Ave|460000|4|3|Luxury condo, high-end amenities
888 Banana Blvd|400000|3|2|Family home with large backyard
999 Coconut Ct|340000|3|2|Newly built, modern architecture
1010 Berry Ln|370000|3|2|Ranch-style house, one-story living
1111 Melon Dr|450000|4|3|Townhouse with community pool
1212 Peach St|380000|3|2|Single-family home in quiet cul-de-sac
1313 Pear Blvd|395000|3|2|Chic apartment in vibrant neighborhood
1414 Plum Pl|405000|3|2|Penthouse with skyline views
"""

df = pd.read_csv(io.StringIO(data), sep='|')
df['price'] = pd.to_numeric(df['price'])

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['description'])

def get_relevant_properties(query, top_n=5):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    relevant_indices = similarities.argsort()[-top_n:][::-1]
    return df.iloc[relevant_indices]

def classify_query(query):
    query = query.lower()
    factual_keywords = ['cheapest', 'most expensive', 'average', 'total', 'maximum', 'most']
    if any(keyword in query for keyword in factual_keywords):
        return 'factual'
    return 'complex'

def get_factual_answer(query, df):
    query = query.lower()
    
    if 'cheapest' in query:
        property = df.loc[df['price'].idxmin()]
        return f"The cheapest property is at {property['address']} priced at ${property['price']:,}, with {property['bedrooms']} bedrooms and {property['bathrooms']} bathrooms."
    
    elif 'most expensive' in query:
        property = df.loc[df['price'].idxmax()]
        return f"The most expensive property is at {property['address']} priced at ${property['price']:,}, with {property['bedrooms']} bedrooms and {property['bathrooms']} bathrooms."
    
    elif 'average price' in query:
        avg_price = df['price'].mean()
        return f"The average price of all properties is ${avg_price:,.0f}."
    
    elif 'total rooms' in query or 'maximum number of rooms' in query:
        total_rooms = df['bedrooms'].sum() + df['bathrooms'].sum()
        return f"The total number of rooms (bedrooms + bathrooms) across all listings is {total_rooms}."
    
    elif 'most rooms' in query or 'most bedrooms and bathrooms' in query:
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']
        property = df.loc[df['total_rooms'].idxmax()]
        return f"The property with the most rooms is at {property['address']} with a total of {property['total_rooms']} rooms ({property['bedrooms']} bedrooms and {property['bathrooms']} bathrooms)."
    
    elif 'average bedrooms' in query:
        avg_bedrooms = df['bedrooms'].mean()
        return f"The average number of bedrooms is {avg_bedrooms:.1f}."
    
    elif 'average bathrooms' in query:
        avg_bathrooms = df['bathrooms'].mean()
        return f"The average number of bathrooms is {avg_bathrooms:.1f}."
    
    elif 'total bedrooms' in query:
        total_bedrooms = df['bedrooms'].sum()
        return f"The total number of bedrooms across all listings is {total_bedrooms}."
    
    elif 'total bathrooms' in query:
        total_bathrooms = df['bathrooms'].sum()
        return f"The total number of bathrooms across all listings is {total_bathrooms}."
    
    elif 'most bedrooms' in query:
        property = df.loc[df['bedrooms'].idxmax()]
        return f"The property with the most bedrooms is at {property['address']} with {property['bedrooms']} bedrooms."
    
    elif 'most bathrooms' in query:
        property = df.loc[df['bathrooms'].idxmax()]
        return f"The property with the most bathrooms is at {property['address']} with {property['bathrooms']} bathrooms."
    
    return None

def verify_response(response, df):
    price_pattern = r'\$(\d{1,3}(,\d{3})*(\.\d+)?)'
    prices = re.findall(price_pattern, response)
    for price_match in prices:
        price = float(price_match[0].replace(',', ''))
        if price < df['price'].min() or price > df['price'].max():
            return f"Warning: The price ${price:,.0f} mentioned in the response seems incorrect. Please verify."
    return response

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

        query_type = classify_query(user_input)

        if query_type == 'factual':
            answer = get_factual_answer(user_input, df)
            context = f"Factual answer: {answer}"
        else:
            relevant_properties = get_relevant_properties(user_input)
            context = f"There are {len(df)} total listings. Here are the top {len(relevant_properties)} relevant properties:\n\n"
            context += relevant_properties.to_string(index=False)

        prompt = f"""Context: {context}

User Question: {user_input}

Please provide an accurate response based on the context and the user's question. Follow these guidelines:
1. Only use information provided in the context.
2. If the question cannot be answered based on the given information, say so.
3. For numerical values, always specify the unit (e.g., dollars, bedrooms, bathrooms).
4. If comparing properties, clearly state the basis of comparison.
5. For questions about totals, averages, or maximums across all listings, use the provided factual answer.

Your response:"""

        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role='user',
            content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )
        
        response = wait_for_run_complete(THREAD_ID, run.id)
        
        verified_response = verify_response(response, df)
        
        return verified_response

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
        return f"Sorry, I encountered an error: {str(e)}"

# Streamlit UI
st.title('A+ Realty and Mortgage Chatbot')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('What would you like to know about our properties?'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = fetch_response(prompt)

    with st.chat_message('assistant'):
        st.markdown(response)

    st.session_state.messages.append({'role': 'assistant', 'content': response})

# Add a feedback mechanism
if st.button('Was this response helpful?'):
    st.write('Thank you for your feedback!')
    # Here you would typically log the feedback for later analysis
