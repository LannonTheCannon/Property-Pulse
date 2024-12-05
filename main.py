# Main.py is a python script designed to show a basic version of the chatbot for
# A+ Mortgage and Lending
#
#########################################################################

import streamlit as st
import openai  # Or another NLP library

# Set up OpenAI API (replace with your key)
openai.api_key = 'sk-WQjJMq6AqYZV6bELhcDWGvEuef2NawLUTpl5dgaB9KT3BlbkFJhL0nGhIC8Uuf8BtydX-QYlFvMmSKvfKxPwUwvZFnwA'

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Basic knowledge base
knowledge_base = {
    "What is a mortgage?": "A mortgage is a loan used to purchase a home, where the property serves as collateral for the loan. The borrower agrees to pay back the loan in regular installments over a set period, usually 15 to 30 years. Mortgages can come with fixed or adjustable interest rates, which impact the total amount paid over the life of the loan.",
    
    "What services does A+ Realty & Mortgage offer?": "A+ Realty & Mortgage offers a range of services including home purchasing assistance, mortgage refinancing, real estate services, and guidance in finding suitable loan agents. They help clients navigate the complexities of buying or refinancing a home, ensuring they find the best mortgage products to meet their needs.",
    
    "How can I get pre-qualified for a mortgage?": "To get pre-qualified for a mortgage, you can fill out the pre-qualification form available on the A+ Realty & Mortgage website. Pre-qualification involves providing basic financial information to give lenders an idea of your borrowing capacity and the loan amount you might qualify for.",
    
    "What is the process for applying for a mortgage?": "Applying for a mortgage with A+ Realty & Mortgage involves several steps: filling out application forms, submitting necessary documents such as income verification and credit history, undergoing a credit review, and working with a loan officer to find the best mortgage options. The process is designed to be thorough yet efficient, ensuring clients receive timely approvals.",
    
    "What types of mortgage loans are available?": "A+ Realty & Mortgage offers various types of mortgage loans including fixed-rate mortgages, which have a constant interest rate and monthly payment; adjustable-rate mortgages (ARMs), which have interest rates that can change periodically; FHA loans, which are insured by the Federal Housing Administration; and VA loans, which are available to veterans and service members.",
    
    "What is an FHA loan?": "An FHA loan is a mortgage insured by the Federal Housing Administration, designed for low-to-moderate income borrowers who may have lower credit scores. FHA loans require a lower minimum down payment and are popular among first-time homebuyers.",
    
    "What is a VA loan?": "A VA loan is a mortgage loan provided by private lenders but guaranteed by the Department of Veterans Affairs. It is designed to offer long-term financing to eligible American veterans or their surviving spouses. VA loans often come with better terms and do not require a down payment or private mortgage insurance (PMI).",
    
    "What is refinancing?": "Refinancing is the process of obtaining a new mortgage to replace an existing one. Borrowers refinance to take advantage of lower interest rates, reduce monthly payments, change the loan term, or cash out equity in their home. A+ Realty & Mortgage provides guidance and options for clients looking to refinance their mortgages.",
    
    "What are current interest rates?": "As of the latest update, interest rates at A+ Realty & Mortgage start at competitive levels for both 30-year fixed and adjustable-rate mortgages. Rates can vary based on market conditions, credit scores, and other factors. For the most current rates, it's best to contact A+ Realty & Mortgage directly or visit their website.",
    
    "How can I contact A+ Realty & Mortgage?": "You can contact A+ Realty & Mortgage by phone at (626) 855-2530 or email them at processor@aplusrm.com. Their office is located at 18725 Gale Ave. Suite 130, City of Industry, CA 91748. They also offer a contact form on their website for inquiries.",
    
    "What is the DRE and NMLS number for A+ Realty & Mortgage?": "A+ Realty & Mortgage's DRE (Department of Real Estate) number is 01428773, and their NMLS (Nationwide Mortgage Licensing System) number is 257581. These numbers certify that they are licensed to provide real estate and mortgage services in their respective jurisdictions.",
    
    "What documents are required for a mortgage application?": "The documents typically required for a mortgage application include proof of income (such as pay stubs, W-2s, or tax returns), credit history, asset information (such as bank statements), and personal identification. A+ Realty & Mortgage provides a detailed list of required documents on their website.",
    
    "What is the pre-approval process?": "The pre-approval process at A+ Realty & Mortgage involves a thorough evaluation of your financial background, including credit score, income, and assets. This process provides a conditional commitment from the lender for a specific loan amount, helping you understand your budget and strengthening your offer when purchasing a home.",
    
    "How does A+ Realty & Mortgage help first-time homebuyers?": "A+ Realty & Mortgage offers special programs and guidance tailored for first-time homebuyers. This includes education on the home buying process, assistance with securing favorable loan terms, and support throughout the mortgage application and approval stages to ensure a smooth and informed purchasing experience.",
    
    "What is an adjustable-rate mortgage (ARM)?": "An adjustable-rate mortgage (ARM) is a type of mortgage with an interest rate that can change periodically based on market conditions. ARMs typically offer lower initial rates compared to fixed-rate mortgages, but the rates can increase or decrease over time, affecting monthly payments.",
    
    "What is private mortgage insurance (PMI)?": "Private mortgage insurance (PMI) is a type of insurance required for conventional loans when the borrower makes a down payment of less than 20% of the home's purchase price. PMI protects the lender in case the borrower defaults on the loan. Borrowers can usually cancel PMI once they have built up enough equity in the home.",
    
    "What are closing costs?": "Closing costs are fees associated with finalizing a mortgage, including loan origination fees, appraisal fees, title insurance, and attorney fees. These costs typically range from 2% to 5% of the loan amount and are paid at the closing of the real estate transaction.",
    
    "What is a credit score, and how does it affect my mortgage application?": "A credit score is a numerical representation of your creditworthiness, based on your credit history. It affects your mortgage application by influencing the interest rates you are offered and your eligibility for certain loan programs. Higher credit scores generally lead to more favorable loan terms.",
    
    "How can I improve my credit score before applying for a mortgage?": "To improve your credit score before applying for a mortgage, you can pay off outstanding debts, make all payments on time, avoid opening new credit accounts, and check your credit report for errors. Consistent and responsible credit behavior over time will help raise your score.",
    
    "What is an amortization schedule?": "An amortization schedule is a table detailing each periodic payment on a mortgage loan. It shows the amount of principal and interest that make up each payment until the loan is paid off. This schedule helps borrowers understand how their payments affect the loan balance over time.",
    
    "What is a rate lock?": "A rate lock is an agreement between the borrower and lender to secure an interest rate for a specific period, typically ranging from 30 to 60 days. This protects the borrower from fluctuations in interest rates during the application and approval process.",
    
    "Can I apply for a mortgage online?": "Yes, A+ Realty & Mortgage offers an online application process. You can start your application by visiting their website and following the steps to fill out the necessary forms and provide required documentation.",
    
    "What is a jumbo loan?": "A jumbo loan is a type of mortgage that exceeds the conforming loan limits set by the Federal Housing Finance Agency (FHFA). These loans are used to finance higher-priced properties and typically have stricter credit requirements and higher interest rates.",
    
    "How do I choose the right mortgage loan?": "Choosing the right mortgage loan depends on your financial situation, long-term goals, and preferences. Factors to consider include the type of loan, interest rates, loan terms, and monthly payments. A+ Realty & Mortgage loan officers can help you evaluate your options and select the best loan for your needs.",
    
    "What is mortgage insurance, and when is it required?": "Mortgage insurance protects the lender in case the borrower defaults on the loan. It is typically required for FHA loans and conventional loans with down payments of less than 20%. There are different types of mortgage insurance, including private mortgage insurance (PMI) and mortgage insurance premiums (MIP) for FHA loans.",
    
    "What should I know about refinancing my mortgage?": "Refinancing your mortgage involves replacing your current loan with a new one, often to secure a lower interest rate, reduce monthly payments, change the loan term, or access home equity. A+ Realty & Mortgage can guide you through the refinancing process and help you decide if it's the right option for you.",
    
    "What is a home appraisal?": "A home appraisal is an assessment of a property's market value conducted by a licensed appraiser. It is required by lenders to ensure the home's value supports the loan amount. The appraisal considers factors such as the home's condition, location, and comparable sales in the area.",
    
    "What is a down payment?": "A down payment is the initial payment made when purchasing a home, typically expressed as a percentage of the property's purchase price. The amount of the down payment affects the loan amount and can influence the interest rate and need for mortgage insurance.",
    
    "How does A+ Realty & Mortgage support clients during the mortgage process?": "A+ Realty & Mortgage supports clients through every step of the mortgage process, from pre-qualification to closing. They offer personalized service, educational resources, and direct access to loan officers to ensure clients makeHere is a detailed and comprehensive knowledge base for A+ Realty & Mortgage based on the available information"
}

# Function to get bot response
def get_bot_response(user_input):
    # In a real implementation, you'd use more sophisticated NLP here
    for question, answer in knowledge_base.items():
        if user_input.lower() in question.lower():
            return answer
    return "I'm sorry, I don't have information on that specific topic. Please ask another question about mortgages."

# Streamlit UI
st.title("Mortgage Chatbot Demo")

# Chat interface
user_input = st.text_input("Ask a question about mortgages:")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Knowledge base update section
st.sidebar.header("Update Knowledge Base")
new_question = st.sidebar.text_input("New Question:")
new_answer = st.sidebar.text_area("New Answer:")
if st.sidebar.button("Add to Knowledge Base"):
    knowledge_base[new_question] = new_answer
    st.sidebar.success("Knowledge base updated!")

# Display current knowledge base
st.sidebar.header("Current Knowledge Base")
st.sidebar.json(knowledge_base)
