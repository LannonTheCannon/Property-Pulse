import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def costs_and_roi():
    st.markdown('<p class="big-font">Costs and ROI Analysis</p>', unsafe_allow_html=True)
    st.write("A Detailed Look at Your Investment and Potential Returns")

    # Cost Breakdown
    st.subheader("Cost Breakdown")
    costs = {
        'Development': 18000,
        'Integration': 5000,
        'Testing': 2000,
        'Deployment': 1000
    }
    
    fig = go.Figure(data=[go.Pie(labels=list(costs.keys()), values=list(costs.values()), hole=.3)])
    fig.update_layout(title_text="Total Investment: $26,000")
    st.plotly_chart(fig, use_container_width=True)

    st.write("Breakdown of costs:")
    for item, cost in costs.items():
        st.write(f"- {item}: ${cost:,}")

    # Payment Structure
    st.subheader("Payment Structure")
    st.write("Four installments of $6,500 over the 5-month implementation period:")
    
    timeline = ['Aug 2024', 'Sep 2024', 'Oct 2024', 'Nov 2024']
    fig = go.Figure(go.Bar(x=timeline, y=[6500]*4, name='Payment'))
    fig.update_layout(title_text="Payment Schedule", xaxis_title="Month", yaxis_title="Amount ($)")
    st.plotly_chart(fig, use_container_width=True)

    # ROI Calculation
    st.subheader("ROI Projection")
    
    # Input assumptions
    st.write("Assumptions for ROI calculation:")
    annual_revenue = st.number_input("Your current annual revenue ($)", value=1000000, step=100000)
    average_sale_value = st.number_input("Average property value ($)", value=300000, step=10000)
    lead_conversion_rate = st.slider("Lead conversion rate (%)", 1, 10, 5) / 100
    customer_service_cost_percentage = st.slider("Current customer service cost (% of revenue)", 1, 10, 5) / 100

    # Projected improvements
    st.write("Projected improvements:")
    lead_increase = st.slider("Expected increase in leads (%)", 10, 50, 30) / 100
    service_cost_reduction = st.slider("Expected reduction in customer service costs (%)", 10, 40, 25) / 100
    
    # Calculations
    current_leads = annual_revenue / average_sale_value
    additional_leads = current_leads * lead_increase
    additional_revenue = additional_leads * lead_conversion_rate * average_sale_value
    current_service_cost = annual_revenue * customer_service_cost_percentage
    service_savings = current_service_cost * service_cost_reduction

    total_benefit = additional_revenue + service_savings
    roi_percentage = (total_benefit - sum(costs.values())) / sum(costs.values()) * 100

    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Investment", f"${sum(costs.values()):,}")
    with col2:
        st.metric("Projected Return (1 year)", f"${total_benefit:,.0f}", delta=f"+{roi_percentage:.0f}%")
    with col3:
        st.metric("Net Profit", f"${total_benefit - sum(costs.values()):,.0f}")

    # Explanation of calculations
    st.write("### How we calculated this:")
    st.write(f"1. Additional Leads: {current_leads:.0f} x {lead_increase:.0%} = {additional_leads:.0f}")
    st.write(f"2. Additional Revenue: {additional_leads:.0f} x {lead_conversion_rate:.0%} x ${average_sale_value:,} = ${additional_revenue:,.0f}")
    st.write(f"3. Service Cost Savings: ${current_service_cost:,.0f} x {service_cost_reduction:.0%} = ${service_savings:,.0f}")
    st.write(f"4. Total Benefit: ${additional_revenue:,.0f} + ${service_savings:,.0f} = ${total_benefit:,.0f}")
    st.write(f"5. ROI: (${total_benefit:,.0f} - ${sum(costs.values()):,}) / ${sum(costs.values()):,} = {roi_percentage:.0f}%")

    # Long-term Value
    st.subheader("Long-term Value")
    st.write("Projected cumulative ROI over 3 years:")
    
    def calculate_cumulative_roi(years):
        cumulative_roi = []
        cumulative_benefit = 0
        for year in range(1, years + 1):
            # Assume benefit increases by 10% each year
            year_benefit = total_benefit * (1.1 ** (year - 1))
            cumulative_benefit += year_benefit
            year_roi = (cumulative_benefit - sum(costs.values())) / sum(costs.values()) * 100
            cumulative_roi.append(year_roi)
        return cumulative_roi

    years = ['Year 1', 'Year 2', 'Year 3']
    cumulative_roi = calculate_cumulative_roi(3)
    
    fig = px.line(x=years, y=cumulative_roi, markers=True)
    fig.update_layout(title='Cumulative ROI Over Time', xaxis_title='Year', yaxis_title='Cumulative ROI (%)')
    st.plotly_chart(fig, use_container_width=True)

    st.write("Assumptions for long-term projection:")
    st.write("- Benefits increase by 10% each year due to compounding effects and system improvements")
    st.write("- No additional major investments are required")

